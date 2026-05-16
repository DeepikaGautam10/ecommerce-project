from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Public URLs
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),

    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Staff management - Category CRUD
    # NOTE: prefixed with "manage/" (not "admin/") to avoid colliding
    # with Django's built-in admin site mounted at /admin/.
    path('manage/categories/', views.category_list, name='category_list'),
    path('manage/categories/create/', views.category_create, name='category_create'),
    path('manage/categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('manage/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Staff management - Product CRUD
    path('manage/products/', views.product_list_admin, name='product_list_admin'),
    path('manage/products/create/', views.product_create, name='product_create'),
    path('manage/products/<int:pk>/update/', views.product_update, name='product_update'),
    path('manage/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
