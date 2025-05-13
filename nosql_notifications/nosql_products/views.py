
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from nosql_products.models_nosql import Product, Category

# GET all products
def get_all_products(request):
    products = Product.objects()
    data = []

    for p in products:
        data.append({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
            "images": p.images,
            "tags": p.tags,
            "available": p.available,
            "category": str(p.category.id) if p.category else None,
        })

    return JsonResponse(data, safe=False)


# POST create product
@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        category = Category.objects(id=body.get("category")).first()

        product = Product(
            name=body.get("name"),
            description=body.get("description"),
            price=body.get("price"),
            stock=body.get("stock", 0),
            category=category,
            images=body.get("images", []),
            tags=body.get("tags", []),
            available=body.get("available", True),
        )
        product.save()

        return JsonResponse({"message": "Product created", "id": str(product.id)}, status=201)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
