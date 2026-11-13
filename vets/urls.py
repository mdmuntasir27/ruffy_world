from django.urls import path
from . import views

urlpatterns = [
    path('', views.vet_list, name='vet_list'),
]

