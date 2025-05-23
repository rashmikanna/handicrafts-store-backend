# project urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import signup
from seller_panel.views import seller_signup

urlpatterns = [
    path('', home),

    # Admin

    path('admin/', admin.site.urls),

    # Auth / Accounts
    path('api/signup/', signup, name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App APIs
    path('api/', include('producer.urls')),
    path('api/usersdata/', include('nosql_usersdata.urls')),
    path('api/notifications/', include('nosql_notifications.urls')),
    path('api/products/', include('nosql_products.urls')),  
    path('api/seller/', include('seller_panel.urls', namespace='seller_panel')),
]

# Serve static and media files in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


