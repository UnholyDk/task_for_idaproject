from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add/', views.ImageCreateView.as_view(), name='image_create'),
    path('<int:pk>/', views.ImageUpdateView.as_view(), name='image_edit')
]