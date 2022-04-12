from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from ulid import ULID

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    age = models.IntegerField(verbose_name="年齢",default=20)
    icon = models.ImageField(
        verbose_name="アイコン", 
        blank= True, 
        upload_to = "profile/icon/", 
        default="profile/icon/default.jpg",
    )
    # user_id =  models.CharField(
    #     verbose_name="ユーザーID",
    #     default= str(ULID()),#str(ULID()),
    #     max_length=26,#primary_key=True,
    #     # editable=False
    # )
    header = models.ImageField(
        verbose_name="プロフィールヘッダー", 
        blank= True, 
        upload_to = "profile/header/", 
        default="profile/header/default.jpg",
    )
