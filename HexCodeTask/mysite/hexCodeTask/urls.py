from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.uploadPhotos, name="photo-upload"),
    path('all/', views.getPhotos, name="getPhotos"),
    path('binary/<int:id>/', views.getBinaryPhoto, name="getBinaryPhoto"),
]
