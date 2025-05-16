from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# JWT views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Your account views
from accounts.views import signup

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth / Accounts
    path('api/signup/', signup, name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('producer.urls')),
]

# In DEBUG mode serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
