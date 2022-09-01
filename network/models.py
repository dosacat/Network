from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime,date

class User(AbstractUser):
    pass

class NetworkPost(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="poster")
    content=models.CharField(max_length=281,blank=False)
    timestamp=models.DateField(auto_now_add=True,auto_now=False,blank=True)
    likes=models.ManyToManyField(User,related_name="liked",blank=True)

    def __str__(self):
        return f"{self.user},{self.content},{self.timestamp},{self.likes}"

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    following=models.ManyToManyField(User,blank=True,related_name="follow")