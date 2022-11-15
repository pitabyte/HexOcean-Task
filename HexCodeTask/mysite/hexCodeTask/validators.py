
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Photo



def expiresIsValid(expires):
    if (int(expires) >= 300 and int(expires) <= 30000):
        return True
    return False

def extensionIsValid(filename):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return True
    return False

def uploadPhotosRequestIsValid(request):
    data = request.data
    if not 'username' in data:
        return Response('Specify "username" in request body', status=status.HTTP_400_BAD_REQUEST)

    if not 'photos' in data:
        return Response('Specify "photos" (files to be uploaded) in request body', status=status.HTTP_400_BAD_REQUEST)

    if not CustomUser.objects.filter(username=data['username']).exists():
        return Response("This username doesn't exists", status=status.HTTP_404_NOT_FOUND)

    user = CustomUser.objects.get(username=data['username'])
    photos = request.FILES.getlist('photos')
    for photo_data in photos:
        photo = Photo(user=user, image=photo_data)
        if not extensionIsValid(photo.image.name):
            return Response('invalid file format', status=status.HTTP_400_BAD_REQUEST)
    return True



    







