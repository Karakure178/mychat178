from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    age = models.IntegerField(verbose_name="年齢",default=20)
    icon = models.ImageField(verbose_name="アイコン", 
    blank= True, 
    upload_to = "profile/icon/", 
    default="profile/icon/default.jpg"
    )