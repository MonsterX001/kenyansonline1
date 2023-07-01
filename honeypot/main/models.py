from datetime import datetime, timezone
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.CharField(max_length=100, default=uuid.uuid4)
    forget_password_token = models.CharField(max_length=1000)
    agentname = models.TextField()
    location = models.TextField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='main_images', default='blank-img.png')
    created_at = models.DateTimeField(auto_now_add=True)
   
    
    def __str__(self):
        return self.user.username
    

class Houseuploads(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.TextField(max_length=100)
    Video_name = models.CharField(max_length=100)
    main_img = models.FileField(upload_to='post_videos')
    details = models.TextField()
    no_of_views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    
    def __str__(self):
        return self.user
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Houseuploads, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    
class Shots(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.TextField(max_length=100)
    Video_name = models.CharField(max_length=100)
    main_img = models.FileField(upload_to='post_videos')
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Views(models.Model):
    post_Id = models.CharField(max_length=500, default=0)
    username = models.CharField(max_length=100)
    

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_link = models.CharField(max_length=200)
    share_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
