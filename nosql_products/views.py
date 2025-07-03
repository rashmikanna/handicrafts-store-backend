# nosql_products/views.py

from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from cloudinary.uploader import upload

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        qs = Product.objects.all()
        p = request.query_params

        cat = p.get('category')
        if cat:
            cat_lower = cat.lower()
            if cat_lower == 'handloom':
                # Match any category whose name contains "loom"
                matched_cats = Category.objects(name__icontains='loom').only('id')
                qs = qs.filter(category__in=[c.id for c in matched_cats])
            elif cat_lower == 'gift':
                # Match only specific categories
                matched_cats = Category.objects(name__in=['Silver Crafts', 'Paintings & Art']).only('id')
                qs = qs.filter(category__in=[c.id for c in matched_cats])
            elif ObjectId.is_valid(cat):
                qs = qs.filter(category=ObjectId(cat))
            else:
                # Match exact category name
                matched_cats = Category.objects(name__iexact=cat).only('id')
                qs = qs.filter(category__in=[c.id for c in matched_cats])


        avail = p.get('available')
        if avail is not None:
            qs = qs.filter(available=(avail.lower() == 'true'))

        min_p = p.get('min_price')
        max_p = p.get('max_price')
        if min_p:
            try:
                qs = qs.filter(price__gte=float(min_p))
            except ValueError:
                pass
        if max_p:
            try:
                qs = qs.filter(price__lte=float(max_p))
            except ValueError:
                pass

        tags_param = p.get('tags')
        if tags_param:
            wanted = [t.strip() for t in tags_param.split(',') if t.strip()]
            if wanted:
                qs = qs.filter(tags__all=wanted)

        q = p.get('q')
        if q:
            qs = qs.filter(__raw__={
                "$or": [
                    {"name": {"$regex": q, "$options": "i"}},
                    {"description": {"$regex": q, "$options": "i"}},
                    {"tags": {"$regex": q, "$options": "i"}},
                ]
            })

        sort = p.get('sort')
        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Pass request into serializer via context so .create() handles owner/category
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.save()
        return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='tags', permission_classes=[permissions.AllowAny])
    def list_tags(self, request):
        all_tags = Product.objects.distinct('tags')
        return Response(all_tags)

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
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        prods = Product.objects.all()
        serializer = ProductSerializer(prods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_seller_products(request):
    user_id = str(request.user.id)
    qs = Product.objects.filter(owner=user_id)
    data = ProductSerializer(qs, many=True).data
    return Response(data)
