from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/<int:pk>/receipt/', views.download_receipt, name='download_receipt'),
    path('my-orders/', views.my_orders, name='my_orders'),
]

