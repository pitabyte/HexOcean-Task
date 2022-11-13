from rest_framework import serializers
from .models import Photo, Thumbnail, BinaryPhoto

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = '__all__'

class BinaryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinaryPhoto
        fields = '__all__'