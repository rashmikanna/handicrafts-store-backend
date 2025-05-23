#urls for seller_panel

from django.urls import path
from .views import seller_signup
#from .views import seller_status


app_name = 'seller_panel'
urlpatterns = [
    path('signup/', seller_signup, name='seller_signup'),
   # path('status/', seller_status, name='seller_status'),
    
]


