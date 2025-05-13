#views for notifications, admin log, error log

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from mongoengine import DoesNotExist, ValidationError

from .models_nosql import UserNotification, AdminLog, ErrorLog
from .serializers import UserNotificationSerializer, AdminLogSerializer, ErrorLogSerializer

#usernotification viewset
class UserNotificationViewSet(viewsets.ViewSet):

    def list(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"message": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        notifications = UserNotification.objects(user_id=user_id)
        serializer = UserNotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        message = request.data.get("message")
        if not user_id or not title:
            return Response({"message": "user_id and title are required."}, status=status.HTTP_400_BAD_REQUEST)
        notification = UserNotification(user_id=user_id, title=title, message=message)
        notification.save()
        return Response({"message": "Notification created."}, status=status.HTTP_201_CREATED)

#adminlog viewset
class AdminLogViewSet(viewsets.ViewSet):

    def list(self, request):
        admin_id = request.query_params.get("admin_id")
        if not admin_id:
            return Response({"message": "admin_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        logs = AdminLog.objects(admin_id=admin_id)
        serializer = AdminLogSerializer(logs, many=True)
        return Response(serializer.data)

    def create(self, request):
        admin_id = request.data.get("admin_id")
        action = request.data.get("action")
        if not admin_id or not action:
            return Response({"message": "admin_id and action are required."}, status=status.HTTP_400_BAD_REQUEST)
        log = AdminLog(admin_id=admin_id, action=action, details=request.data.get("details"))
        log.save()
        return Response({"message": "Admin log created."}, status=status.HTTP_201_CREATED)

# errorlog viewset
class ErrorLogViewSet(viewsets.ViewSet):

    def list(self, request):
        error_type = request.query_params.get("error_type")
        if not error_type:
            return Response({"message": "error_type is required."}, status=status.HTTP_400_BAD_REQUEST)
        logs = ErrorLog.objects(error_type=error_type)
        serializer = ErrorLogSerializer(logs, many=True)
        return Response(serializer.data)

    def create(self, request):
        error_type = request.data.get("error_type")
        message = request.data.get("message")
        if not error_type or not message:
            return Response({"message": "error_type and message are required."}, status=status.HTTP_400_BAD_REQUEST)
        error_log = ErrorLog(error_type=error_type, message=message)
        error_log.save()
        return Response({"message": "Error log created."}, status=status.HTTP_201_CREATED)
