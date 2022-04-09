from django.db import models
#from django.contrib.auth.models import User
from users.models import User
# from django.contrib.auth import get_user_model
# from django.contrib.postgres.fields import ArrayField

class Room(models.Model):
    room = models.CharField('トークルーム', max_length=10)
    meta = models.ManyToManyField("users.User",related_name = "add_users")

    def __str__(self):
        return self.room

class Chat(models.Model):
    name = models.CharField('ユーザー名', max_length=255)
    models.ForeignKey(User, verbose_name='名前', related_name='impressions', on_delete=models.CASCADE)
    room = models.CharField('トークルーム', max_length=10)
    text = models.CharField('テキストの入力', blank=True, max_length=144)
    time = models.DateTimeField('送られた時間' ,auto_now=True)


class Article(models.Model):
    title = models.CharField(max_length=100)
    meta = models.ManyToManyField('Tag')

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField("タグ名",max_length=30)
    def __str__(self):
        return self.name




#from django.db import models
#from users.models import User
# from distutils.command.upload import upload
# from email.policy import default
# from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.fields import ArrayField

# class Tag(models.Model):
#     name = models.CharField(unique=True, max_length=64)
#     def __str__(self):
#         return self.name

# class User(AbstractUser):
#     class Meta:
#         db_table = 'auth_user'
#     age = models.IntegerField(verbose_name="年齢",default=20)
#     icon = models.ImageField(
#         verbose_name="アイコン", 
#         blank= True, 
#         upload_to = "profile/icon/", 
#         default="profile/icon/default.jpg"
#     )
    # followees = models.ManyToManyField(
    #     'User', 
    #     verbose_name='フォロー中のユーザー', 
    #     through='FriendShip',
    #     related_name='+', 
    #     through_fields=('follower', 'followee')
    # )
    # followers = models.ManyToManyField(
    #     'User', 
    #     verbose_name='フォローしてきているユーザー', 
    #     through='FriendShip', 
    #     related_name='+', 
    #     through_fields=('followee', 'follower')
    # )
#     tags = models.ManyToManyField(
#         "Tag",
#         verbose_name='タグ',
#         related_name='+'
#     )

# class Article(models.Model):
#     title = models.CharField(max_length=128)
#     tags  = models.ManyToManyField(Tag)

#     def __str__(self):
#         return self.title


#フォロー機能中間テーブル
# class FriendShip(models.Model):
#     follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followee_friendships')
#     followee = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower_friendships')

#     class Meta:
#         unique_together = ('follower', 'followee')


# class ManyTest(models.Model):
#     test = models.ForeignKey('User', on_delete=models.CASCADE)
#     age = models.IntegerField(verbose_name="年齢",default=20)

