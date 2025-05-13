#urls for notifications, admin log, error log

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserNotificationViewSet, AdminLogViewSet, ErrorLogViewSet

router = DefaultRouter()
router.register(r'user-notifications', UserNotificationViewSet, basename='user-notification')
router.register(r'admin-logs', AdminLogViewSet, basename='admin-log')
router.register(r'error-logs', ErrorLogViewSet, basename='error-log')

urlpatterns = [
    path('', include(router.urls)),  
]
