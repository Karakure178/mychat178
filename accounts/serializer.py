from rest_framework import serializers
from users.models import User
from accounts.models import Chat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    icon = UserSerializer()
    class Meta:
        model = Chat
        fields = ('name', 'room', 'text', 'time', 'icon')