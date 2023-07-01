from django.contrib import admin
from .models import Profile, Houseuploads, Shots, Views, Comment, FollowersCount


# Register your models here.
admin.site.register(Profile)
admin.site.register(Houseuploads)
admin.site.register(Shots)
admin.site.register(Views)
admin.site.register(Comment)
admin.site.register(FollowersCount)

