from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from rest_framework.decorators import api_view
from .models import Photo, CustomUser, Thumbnail, BinaryPhoto
from .serializers import PhotoSerializer, ThumbnailSerializer, BinaryPhotoSerializer
from PIL import Image, ImageOps
import json
import io
from datetime import timezone, timedelta, datetime
from django.http import JsonResponse
from hexCodeTask.helpers import expiresIsValid, getImageURL, extensionIsValid
import os
# Create your views here.

@api_view(['GET'])
def index(request):
    return Response("Hello world")

@api_view(['GET'])
def getPhotos(request):
    data = request.data
    username = data['username']
    password = data['password']
    user = CustomUser.objects.get(username=username, password=password)
    #photos = Photo.objects.filter(user=user)
    #serializer = PhotoSerializer(photos, many=True)
    #return Response(serializer.data)
    response = []
    baseURL = request.build_absolute_uri(reverse('index'))
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

@api_view(['GET'])
def getPhoto(request, id):
    if Photo.objects.filter(id=id).exists():
        photo = Photo.objects.get(id=id)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)
    else:
        content = {"This photo doesn't exist"}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def uploadPhoto(request):
    data = request.data
    username = data['username']
    password = data['password']
    user = CustomUser.objects.get(username=username, password=password)

    response = {}
    responseList = []
    baseURL = request.build_absolute_uri(reverse('index'))

    photos = request.FILES.getlist('photos')
    for photo_data in photos:
        photo = Photo(user=user, image=photo_data)
        print(photo.image.name)
        #if not extensionIsValid(photo.getFilename()):
            
        if not extensionIsValid(photo.image.name):
            return HttpResponse('invalid file format')
        photo.save()
        heights = user.tier.get_heights_list()
        for height in heights:
            photo.createThumbnailFile(height)
            url = photo.getNewURL(baseURL, height)
            thumbnail = Thumbnail(user=user, photo=photo, height=height, url=url)
            thumbnail.save()
            response["thumbnail" + height] = url

        if (user.tier.expiring_link == True and 'expires' in data):
            if expiresIsValid(data['expires']):
                binaryPhoto = photo.createBinary(user)
                binaryPhoto.url = binaryPhoto.getURL(baseURL)
                binaryPhoto.expires = data['expires']
                binaryPhoto.save()
                response['binary'] = binaryPhoto.url
            else:
                return HttpResponse('invalid "expires" value')

        if (user.tier.gets_original == True):
            photo.appendURLtoResponse(response, baseURL)
        else:
            os.remove(photo.image.path)
        responseList.append(response.copy())
        response.clear()
    #return Response(responseList)
    return JsonResponse(responseList, safe=False)
    return Response('photo was uploaded')

@api_view(['GET'])
def getBinaryPhoto(request, id):
    binaryPhoto = BinaryPhoto.objects.get(id=id)
    difference = (datetime.now(timezone.utc) - binaryPhoto.date).total_seconds()

    if (difference < binaryPhoto.expires):
        img = open(binaryPhoto.path, 'rb')
        response = FileResponse(img)
        return response
    else:
        os.remove(binaryPhoto.path)
        binaryPhoto.delete()
        return HttpResponse("This image has already expired")

