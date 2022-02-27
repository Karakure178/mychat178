from django.contrib import admin
from . import models

# Register your models here.
#これ追加しないとadminサイトから確認できない
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room",)
admin.site.register(models.Room,RoomAdmin)

class ChatAdmin(admin.ModelAdmin):
    list_display = ("name","room","text","time")
admin.site.register(models.Chat,ChatAdmin)