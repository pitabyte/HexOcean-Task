from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Photo, CustomUser, Thumbnail, BinaryPhoto
from .serializers import PhotoSerializer, ThumbnailSerializer, BinaryPhotoSerializer
from PIL import Image, ImageOps
import json
import io
from datetime import timezone, timedelta, datetime
from django.http import JsonResponse
from hexCodeTask.validators import expiresIsValid, extensionIsValid, uploadPhotosRequestIsValid
import os
# Create your views here.

@api_view(['GET'])
def getPhotos(request, username):
    if not CustomUser.objects.filter(username=username).exists():
        return Response("This user doesn't exist", status=status.HTTP_404_NOT_FOUND)
    user = CustomUser.objects.get(username=username)
    response = []
    baseURL = request.build_absolute_uri('/')
    photos = Photo.objects.filter(user=user)
    thumbnails = Thumbnail.objects.filter(user=user)
    binaries = BinaryPhoto.objects.filter(user=user)

    for photo in photos:
        response.append(photo.getURL(baseURL))
    for thumb in thumbnails:
        response.append(thumb.url)
    for binary in binaries:
        response.append(binary.url)
    return JsonResponse(response, safe=False)

@api_view(['POST'])
def uploadPhotos(request):
    data = request.data
    if not uploadPhotosRequestIsValid(request) == True:
        return uploadPhotosRequestIsValid(request)
    user = CustomUser.objects.get(username=data['username'])
    response = {}
    responseList = []
    baseURL = request.build_absolute_uri('/')
    photos = request.FILES.getlist('photos')

    for photo_data in photos:
        photo = Photo(user=user, image=photo_data)
        photo.save()

        heights = user.tier.get_heights_list()
        for height in heights:
            thumbnail = photo.createThumbnail(height, baseURL)
            response["thumbnail" + height] = thumbnail.url

        if (user.tier.expiring_link == True and 'expires' in data):
            if expiresIsValid(data['expires']):
                binaryPhoto = photo.createBinary(data['expires'], baseURL)
                response['binary'] = binaryPhoto.url
            else:
                return Response('invalid "expires" value', status=status.HTTP_400_BAD_REQUEST)

        if (user.tier.gets_original == True):
             response['original'] = photo.getURL(baseURL)
        else:
            os.remove(photo.image.path)

        responseList.append(response.copy())
        response.clear()
    return JsonResponse(responseList, safe=False)

@api_view(['GET'])
def getBinaryPhoto(request, id):
    if not BinaryPhoto.objects.filter(id=id).exists():
        return Response("this photo doesn't exist", status=status.HTTP_404_NOT_FOUND)
    binaryPhoto = BinaryPhoto.objects.get(id=id)
    difference = (datetime.now(timezone.utc) - binaryPhoto.date).total_seconds()

    if (difference < binaryPhoto.expires):
        try:
            img = open(binaryPhoto.path, 'rb')
            response = FileResponse(img)
            return response
        except IOError:
            return HttpResponse("File not found", status=status.HTTP_404_NOT_FOUND)
    else:
        os.remove(binaryPhoto.path)
        binaryPhoto.delete()
        return HttpResponse("This image has already expired", status=status.HTTP_404_NOT_FOUND)

