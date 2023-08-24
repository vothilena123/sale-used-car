from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.db.models import Q
# Create your models here.

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userID = models.IntegerField()
    about = models.TextField(blank=True)
    profileImage = models.ImageField(upload_to = 'profile_images', default='default-avatar-profile.jpeg')
    backgroundImage = models.ImageField(upload_to = 'profile_images', default='default-background.jpeg')
    location = models.CharField(max_length = 100, blank=True)
    detailAdress = models.CharField(max_length = 150, blank=True)
    phoneNumber = models.CharField(max_length = 100, blank=True)


    def __str__(self):
        return self.user.username


class PostSell(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    carName = models.CharField(max_length=100)
    image1 = models.ImageField(upload_to='post_images')
    yearOfManufacture = models.IntegerField()
    carStatus = models.CharField(max_length=100)
    transmission = models.CharField(max_length=100)
    fuel = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    kilimetersRun = models.IntegerField()
    locationSell = models.CharField(max_length=100)
    carPrice = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    createdAt = models.DateTimeField(default=datetime.now)
    numberOfLike = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class PostSellImages(models.Model):
    id=models.AutoField(primary_key=True)
    post_id = models.ForeignKey(PostSell,on_delete=models.CASCADE)
    carImage = models.FileField(upload_to='post_images')

    def __uuid__(self):
        return self.user



class LikePost(models.Model):
    post_liked_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs
        

class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)