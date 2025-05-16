import base64
from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.conf import settings

# Connect to MongoDB Atlas
client = MongoClient(settings.MONGODB_URI)
db = client["telangana_handicrafts_db"]
collection = db["products"]

@api_view(['POST'])
def upload_image(request):
    image_file = request.FILES.get('image')
    name = request.POST.get('name')

    if not image_file or not name:
        return Response({"error": "Image and name required"}, status=400)

    try:
        # Convert image to base64
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

        # Create new product document with image
        new_product = {
            "name": name,
            "images": [{
                "data": image_data,
                "content_type": image_file.content_type,
                "display_name": name
            }],
            "available": False,  # Set as not available until other details are filled
        }

        result = collection.insert_one(new_product)

        return Response({
            "message": "Image uploaded and product created",
            "product_id": str(result.inserted_id)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
