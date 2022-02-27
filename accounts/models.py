from django.db import models
#from django.contrib.auth.models import User
from users.models import User

# Create your models here.
#どんなルームがあるか保存
class Room(models.Model):
    room = models.CharField('トークルーム', max_length=255)
    def __str__(self):
        return self.room

class Chat(models.Model):
    name = models.CharField('ユーザー名', max_length=255)
    models.ForeignKey(User, verbose_name='名前', related_name='impressions', on_delete=models.CASCADE)
    room = models.CharField('トークルーム', max_length=255)
    text = models.CharField('テキストの入力', blank=True, max_length=144)
    time = models.DateTimeField('送られた時間' ,auto_now=True)