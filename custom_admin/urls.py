from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Auth
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Pets
    path('pets/', views.pet_list_view, name='pet_list'),
    path('pets/add/', views.pet_add_view, name='pet_add'),
    path('pets/<int:pk>/edit/', views.pet_edit_view, name='pet_edit'),
    path('pets/<int:pk>/delete/', views.pet_delete_view, name='pet_delete'),

    # Adoptions
    path('adoptions/', views.adoption_list_view, name='adoption_list'),
    path('adoptions/<int:pk>/', views.adoption_detail_view, name='adoption_detail'),
    path('adoptions/<int:pk>/delete/', views.adoption_delete_view, name='adoption_delete'),

    # Store Products
    path('products/', views.product_list_view, name='product_list'),
    path('products/add/', views.product_add_view, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete_view, name='product_delete'),

    # Store Orders
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:pk>/delete/', views.order_delete_view, name='order_delete'),

    # Vets
    path('vets/', views.vet_list_view, name='vet_list'),
    path('vets/add/', views.vet_add_view, name='vet_add'),
    path('vets/<int:pk>/edit/', views.vet_edit_view, name='vet_edit'),
    path('vets/<int:pk>/delete/', views.vet_delete_view, name='vet_delete'),

    # Community Posts & Inquiries
    path('community/posts/', views.community_post_list_view, name='community_post_list'),
    path('community/posts/<int:pk>/delete/', views.community_post_delete_view, name='community_post_delete'),
    path('community/inquiries/', views.community_inquiry_list_view, name='community_inquiry_list'),
    path('community/inquiries/<int:pk>/', views.community_inquiry_detail_view, name='community_inquiry_detail'),
    path('community/inquiries/<int:pk>/delete/', views.community_inquiry_delete_view, name='community_inquiry_delete'),

    # Users
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
]
