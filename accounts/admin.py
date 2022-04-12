from django.contrib import admin
from . import models

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room','_meta')

    def _meta(self, row):
        return ','.join([x.username for x in row.meta.all()])
admin.site.register(models.Room,RoomAdmin)

class ChatAdmin(admin.ModelAdmin):
    list_display = ("name","room","text","time","icon")
admin.site.register(models.Chat,ChatAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
admin.site.register(models.Tag, TagAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', '_meta')

    def _meta(self, row):
        return ','.join([x.name for x in row.meta.all()])
admin.site.register(models.Article, ArticleAdmin)







#from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
#from django.utils.translation import gettext_lazy as _

#from .models import ManyTest, User
#Tag, Article, 

# class followersInlineAdmin(admin.TabularInline):
#     model = User.followers.through
#     fk_name = "follower"


# class FolloweesInlineAdmin(admin.TabularInline):
#     model = User.followees.through
#     fk_name = "followee"

# class CustomUserAdmin(UserAdmin):
#     fieldsets   = (
#             (None,{"fields":("username","password")}),
#             (_("Personal info"),{"fields":("first_name","last_name","email","age","icon","tags")}),
#             (_("Permissions"),{"fields":("is_active","is_staff","is_superuser","groups","user_permissions")}),
#             (_("Important dates"),{"fields":("last_login","date_joined")}),
#     )
    #inlines = (followersInlineAdmin,FolloweesInlineAdmin)

# class ArticleAdmin(admin.ModelAdmin):
#     fields = ["title","tags"]

# admin.site.register(Article, ArticleAdmin)
# admin.site.register(Tag)

# admin.site.register(User, CustomUserAdmin)
#admin.site.register(ManyTest)

