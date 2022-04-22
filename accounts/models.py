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
    #models.ForeignKey(User, verbose_name='名前', related_name='impressions', on_delete=models.CASCADE)
    room = models.CharField('トークルーム', max_length=10)
    text = models.CharField('テキストの入力', blank=True, max_length=144)
    time = models.DateTimeField('送られた時間' ,auto_now=True)
    icon = models.ForeignKey(User, on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField(max_length=100)
    meta = models.ManyToManyField('Tag')

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField("タグ名",max_length=30)
    def __str__(self):
        return self.name
