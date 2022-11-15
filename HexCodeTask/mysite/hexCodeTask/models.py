from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image, ImageOps
import os

# Create your models here.

class Tier(models.Model):
    name = models.CharField(max_length=20)
    heights = models.CharField(max_length=20)
    gets_original = models.BooleanField(null=True)
    expiring_link = models.BooleanField(null=True)

    def __str__(self):
         return self.name

    def get_heights_list(self):
        heights_list = self.heights.split()
        return heights_list

class CustomUser(AbstractUser):
    pass
    tier = models.ForeignKey(Tier, on_delete=models.DO_NOTHING, null=True)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos', null=True)
    image = models.ImageField(null=True, blank=True, upload_to=user_directory_path)

    def getFilename(self):
        return os.path.basename(self.image.path)

    def getNewFilename(self, height=None):
        if height:
            filename = "T" + str(height) + "-" + self.getFilename()
        else:
            filename = "B-" + self.getFilename()
        return filename

    def createThumbnail(self, height, baseURL):
        image = Image.open(self.image.path)
        ratio = image.width / image.height
        MAX_SIZE = (float(height) * ratio, int(height))
        image.thumbnail(MAX_SIZE)
        path = self.getNewPath(height)
        image.save(path, format='JPEG')
        url = self.getNewURL(baseURL, height)
        thumbnail = Thumbnail(user=self.user, photo=self, height=height, url=url)
        thumbnail.save()
        return thumbnail

    def getNewPath(self, height=None):
        if height:
            filename = self.getNewFilename(height)
        else:
            filename = self.getNewFilename()
        dir = os.path.dirname(self.image.path)
        path = dir + "/" + filename
        return path
        
    def getNewURL(self, baseURL, height):
        filename = self.getNewFilename(height)
        return baseURL + "static/images/user_{0}/{1}".format(self.user.id, filename)

    def createBinary(self, expires, baseURL):
        image = Image.open(self.image.path)
        grayImage = ImageOps.grayscale(image)
        path = self.getNewPath()
        grayImage.save(path, format='JPEG')
        binaryPhoto = BinaryPhoto(user=self.user, photo=self, path=path)
        binaryPhoto.save()
        binaryPhoto.url = binaryPhoto.getURL(baseURL)
        binaryPhoto.expires = expires
        binaryPhoto.save()
        return binaryPhoto
    
    def getURL(self, baseURL):
        return baseURL + "static/images/user_{0}/{1}".format(self.user.id, self.getFilename())

class Thumbnail(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='thumbnails', null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='thumbnails', null=True)
    height = models.IntegerField(null=True)
    url = models.CharField(max_length=40, null=True)


class BinaryPhoto(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='binary', null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='binary', null=True)
    url = models.CharField(max_length=40, null=True)
    expires = models.IntegerField(validators=[MinValueValidator(300), MaxValueValidator(30000)], null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    path = models.CharField(max_length=100, null=True)


    def getURL(self, baseURL):
        return baseURL + "binary/" + str(self.id)

    

