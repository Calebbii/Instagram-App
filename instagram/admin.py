from django.contrib import admin
from instagram.models import Image,Profile,Comments,Likes, Follows

# Register your models here.
admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Follows)