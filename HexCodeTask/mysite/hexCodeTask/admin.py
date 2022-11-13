from django.contrib import admin

from .models import CustomUser, Photo, Tier
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Photo)
admin.site.register(Tier)