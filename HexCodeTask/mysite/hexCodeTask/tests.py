
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from io import BytesIO
from PIL import Image, ImageOps
from .models import CustomUser, Photo, Tier, BinaryPhoto, Thumbnail
from rest_framework.test import APIRequestFactory
from .validators import uploadPhotosRequestIsValid, expiresIsValid, extensionIsValid
from rest_framework.decorators import api_view

# Create your tests here.

def get_test_tier():
    tier = Tier(heights="1000 500", gets_original=False, expiring_link=False)
    tier.save()
    return tier

def get_test_user(tier):
    user = CustomUser(username='adam', tier=tier)
    user.save()
    return user


class PhotoTestCase(APITestCase):
    
    def test_expiresIsValid(self):
        self.assertEqual(expiresIsValid(10), False)
        self.assertEqual(expiresIsValid(35000), False)
        self.assertEqual(expiresIsValid(50), True)

    def test_extensionIsValid(self):
        self.assertEqual(extensionIsValid('photo.txt'), False)
        self.assertEqual(extensionIsValid('photo.jpg'), True)
        

    def test_get_photos_should_fail(self):
        response = self.client.get(reverse('getPhotos', kwargs={'username':'hello'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_photos_should_pass(self):
        tier = get_test_tier()
        user = get_test_user(tier)
        response = self.client.get(reverse('getPhotos', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

