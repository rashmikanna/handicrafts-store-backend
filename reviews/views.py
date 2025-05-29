# reviews/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from pymongo import MongoClient
import datetime

# Initialize MongoClient just once at the module level
mongo_client = MongoClient(settings.MONGO_URI)
db = mongo_client[settings.MONGO_DB_NAME]
reviews_collection = db['reviews']

def serialize_review(review):
    return {
        "id": str(review.get("_id")),
        "product_id": review.get("product_id"),
        "user": review.get("user"),
        "rating": review.get("rating"),
        "comment": review.get("comment"),
        "created_at": review.get("created_at").isoformat() if review.get("created_at") else None,
    }

class ProductReviews(APIView):
    # You can add authentication & permissions here as before

    def get(self, request, product_id):
        reviews_cursor = reviews_collection.find({"product_id": product_id}).sort("created_at", -1)
        reviews = [serialize_review(r) for r in reviews_cursor]
        return Response(reviews)

    def post(self, request, product_id):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        user = request.user.username
        rating = data.get("rating")
        comment = data.get("comment")

        if rating is None or comment is None:
            return Response({"detail": "Rating and comment are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return Response({"detail": "Rating must be 1 to 5."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "Invalid rating."}, status=status.HTTP_400_BAD_REQUEST)

        review_doc = {
            "product_id": product_id,
            "user": user,
            "rating": rating,
            "comment": comment,
            "created_at": datetime.datetime.utcnow()
        }

        result = reviews_collection.insert_one(review_doc)
        new_review = reviews_collection.find_one({"_id": result.inserted_id})

        return Response(serialize_review(new_review), status=status.HTTP_201_CREATED)
