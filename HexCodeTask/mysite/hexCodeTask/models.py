from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class Tier(models.Model):
    name = models.CharField(max_length=20)
    heights = models.CharField(max_length=20)
    gets_original = models.BooleanField(null=True)
    gets_link = models.BooleanField(null=True)
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

    def appendURLtoResponse(self, response, baseURL):
        finalURL = baseURL + "static" + self.image.url
        response['original'] = finalURL

class Thumbnail(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='thumbnails', null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='thumbnails', null=True)
    height = models.IntegerField(null=True)
    url = models.CharField(max_length=40, null=True)

    def appendURLtoResponse(self, response, baseURL):
        finalURL = baseURL + "thumbnail/" + str(self.id)
        key = "thumbnail" + str(self.height)
        response[key] = finalURL

class BinaryPhoto(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='binary', null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='binary', null=True)
    url = models.CharField(max_length=40, null=True)
    expires = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(30000)])
    date = models.DateTimeField(auto_now_add=True, null=True)
    path = models.CharField(max_length=100, null=True)

    
    def appendURLtoResponse(self, response, baseURL):
        finalURL = baseURL + "binary/" + str(self.id)
        response['binary'] = finalURL

    

