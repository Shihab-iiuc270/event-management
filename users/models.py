from django.db import models
from django.contrib.auth.models import AbstractUser,User
# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images',blank=True,default='profile_images/default.png')
    phone_number = models.CharField(max_length=15,null=True,blank=True,unique=True)
    bio = models.TextField(blank=True)


    def __str__(self):
        return self.username