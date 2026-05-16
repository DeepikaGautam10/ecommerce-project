from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Customer
    path('checkout/', views.checkout_view, name='checkout'),
    path('my-orders/', views.order_list_view, name='order_list'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),

    # Staff order management
    path('manage/', views.manage_order_list, name='manage_order_list'),
    path('manage/<int:order_id>/status/', views.manage_order_update_status,
         name='manage_order_update_status'),
]
