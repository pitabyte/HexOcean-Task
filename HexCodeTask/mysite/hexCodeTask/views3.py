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
from hexCodeTask.helpers import expiresIsValid, getImageURL
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
    photos = Photo.objects.filter(user=user)
    serializer = PhotoSerializer(photos, many=True)
    return Response(serializer.data)

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
        print(photo.getFilename())
        photo.save()

        heights = user.tier.get_heights_list()
        for height in heights:
            thumbnail = createThumbnail(photo, height)
            filename = "T" + str(height) + "-" + os.path.basename(photo.image.path)
            dir = os.path.dirname(photo.image.path)
            path = dir + "/" + filename
            image.save(path, format='JPEG')

            
            key = "thumbnail" + height
            url = getImageURL(baseURL, filename, photo)
            thumbnail = Thumbnail(user=user, photo=photo, height=height, url=url)
            thumbnail.save()
            response[key] = url


        if (user.tier.expiring_link == True and 'expires' in data):
            if expiresIsValid(data['expires']):
                
                image = Image.open(photo.image.path)
                grayImage = ImageOps.grayscale(image)
                filename = "B" + str(height) + "-" + os.path.basename(photo.image.path)
                dir = os.path.dirname(photo.image.path)
                path = dir + "/" + filename
                grayImage.save(path, format='JPEG')
                key = "binary" + height
                
                binaryPhoto = BinaryPhoto(user=user, photo=photo, expires=data['expires'], path=path)
                binaryPhoto.save()
                finalURL = baseURL + "binary/" + str(binaryPhoto.id)
                binaryPhoto.url = finalURL
                binaryPhoto.save()
                response['binary'] = finalURL
            else:
                return HttpResponse('invalid "expires" value')

        if (user.tier.gets_original == True):
            photo.appendURLtoResponse(response, baseURL)
        else:
            os.remove(photo.image.path)

        responseList.append(response.copy())
        response.clear()
    
    return Response(responseList)
    return Response('photo was uploaded')

@api_view(['GET'])
def getThumbnail(request, id):
    thumbnail = Thumbnail.objects.get(id=id)
    image = Image.open(thumbnail.photo.image.path)
    ratio = image.width / image.height
    MAX_SIZE = (thumbnail.height * ratio, thumbnail.height)
    image.thumbnail(MAX_SIZE)
    output = io.BytesIO()
    image.save(output, format='JPEG')
    print(image.width)
    print(image.height)
    hex_data = output.getvalue()
    return HttpResponse(hex_data, content_type="image/jpeg")

@api_view(['GET'])
def getBinaryPhoto(request, id):
    binaryPhoto = BinaryPhoto.objects.get(id=id)
    difference = (datetime.now(timezone.utc) - binaryPhoto.date).total_seconds()
    if (difference < binaryPhoto.expires):
        img = open(binaryPhoto.path, 'rb')

        response = FileResponse(img)

        return response
        
    else:
        return HttpResponse("This image has already expired")