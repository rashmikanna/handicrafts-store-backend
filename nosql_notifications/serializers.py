#serializers for notifications, admin log, error log

from rest_framework import serializers
from .models_nosql import UserNotification, AdminLog, ErrorLog
from bson import ObjectId

#custom serializer field to handle ObjectId
class ObjectIdField(serializers.CharField):
    def to_representation(self, value):
        #convert ObjectId to string
        if isinstance(value, ObjectId):
            return str(value)
        return super().to_representation(value)


class UserNotificationSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    user_id = ObjectIdField()
    title = serializers.CharField()
    message = serializers.CharField(allow_blank=True, required=False)
    created_at = serializers.DateTimeField()
    read = serializers.BooleanField()

class AdminLogSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    admin_id = ObjectIdField()
    action = serializers.CharField()
    details = serializers.CharField(allow_blank=True, required=False)
    timestamp = serializers.DateTimeField()

class ErrorLogSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    error_type = serializers.CharField()
    message = serializers.CharField(allow_blank=True, required=False)
    occurred_at = serializers.DateTimeField()
