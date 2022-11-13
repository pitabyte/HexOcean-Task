from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.uploadPhoto, name="photo-upload"),
    path('all/', views.getPhotos, name="getPhotos"),
    path('thumbnail/<int:id>/', views.getThumbnail, name="getThumbnail"),
    path('binary/<int:id>/', views.getBinaryPhoto, name="getBinaryPhoto")
]
