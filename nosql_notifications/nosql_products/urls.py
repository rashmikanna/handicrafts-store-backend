
from django.urls import path
from . import views

urlpatterns = [

    # category urls
    path('categories/', views.get_all_categories, name='category_list'),
    path('categories/create/', views.create_category, name='category_create'),
    path('categories/<str:category_id>/', views.get_category_by_id, name='category_detail'),
    path('categories/<str:category_id>/update/', views.update_category, name='category_update'),
    path('categories/<str:category_id>/delete/', views.delete_category, name='category_delete'),

    # product urls
    path('', views.get_all_products, name='product_list'),
    path('create/', views.create_product, name='product_create'),
    path('<str:product_id>/', views.get_product_by_id, name='product_detail'),
    path('<str:product_id>/update/', views.update_product, name='product_update'),
    path('<str:product_id>/delete/', views.delete_product, name='product_delete'),
    path('search/',views.search_products, name='product_search'),

]
