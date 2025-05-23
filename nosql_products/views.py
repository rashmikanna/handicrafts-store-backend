# nosql_products/views.py

from bson import ObjectId
from cloudinary.uploader import upload
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models_nosql import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def filter_by_name(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response(
                {"message": "Please provide a category name to filter."},
                status=status.HTTP_400_BAD_REQUEST
            )
        cats = Category.objects(name__icontains=name)
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if not ObjectId.is_valid(pk):
            return Response({"error": "Invalid category ID format"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            cat = Category.objects.get(id=ObjectId(pk))
        except Category.DoesNotExist:
            return Response({"error": "Category not found"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(cat)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        qs = Product.objects.all()
        filters = {}

        # category filter
        cat = request.query_params.get('category')
        if cat:
            if ObjectId.is_valid(cat):
                try:
                    cat_obj = Category.objects.get(id=ObjectId(cat))
                except Category.DoesNotExist:
                    return Response({"detail": "Category not found."},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                cat_obj = Category.objects(name__icontains=cat).first()
                if not cat_obj:
                    return Response({"detail": "Category not found."},
                                    status=status.HTTP_404_NOT_FOUND)
            filters['category'] = cat_obj

        # price range
        try:
            min_p = request.query_params.get('min_price')
            max_p = request.query_params.get('max_price')
            if min_p:
                filters['price__gte'] = float(min_p)
            if max_p:
                filters['price__lte'] = float(max_p)
        except ValueError:
            raise ValidationError({"detail": "min_price and max_price must be numbers."})

        # availability only when true
        if request.query_params.get('available') == 'true':
            filters['available'] = True

        qs = qs.filter(**filters)

        # Full-text search using regex
        q = request.query_params.get('q')
        if q:
            qs = qs.filter(__raw__={
                "$or": [
                    {"name": {"$regex": q, "$options": "i"}},
                    {"description": {"$regex": q, "$options": "i"}},
                    {"tags": {"$regex": q, "$options": "i"}}
                ]
            })

        # sorting
        sort = request.query_params.get('sort')
        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
        else:
            qs = qs.order_by('-created_at')

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        cat_id = self.request.data.get('category')
        cat = Category.objects.filter(id=cat_id).first()
        if not cat:
            raise ValidationError({"message": "Invalid category reference."})
        serializer.save(category=cat)

    def retrieve(self, request, pk=None):
        if not ObjectId.is_valid(pk):
            return Response({"error": "Invalid product ID format"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            prod = Product.objects.get(id=ObjectId(pk))
        except Product.DoesNotExist:
            return Response({"error": "Product not found"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(prod)
        return Response(serializer.data)


@csrf_exempt
def upload_image(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=405)
    image = request.FILES.get('image')
    if not image:
        return JsonResponse({"error": "No image provided"}, status=400)
    try:
        resp = upload(image)
        return JsonResponse({"image_url": resp.get('secure_url')}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Cloudinary upload failed: {e}"}, status=500)


class ProductListView(APIView):
    """Legacy list-all view if you still need it."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        prods = Product.objects.all()
        serializer = ProductSerializer(prods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TempSellerProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects(owner="temp_seller")

    def perform_create(self, serializer):
        serializer.save(owner="temp_seller")

    def retrieve(self, request, pk=None):
        if not ObjectId.is_valid(pk):
            return Response({"detail": "Invalid ID format."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            ps = Product.objects.get(id=ObjectId(pk))
        except Product.DoesNotExist:
            return Response({"detail": "Not found."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(ps)
        return Response(serializer.data)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow reads for anyone; writes only for owners."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == str(request.user.id)
