from django.urls import path

from . import views

urlpatterns = [
    path( '', views.chat, name='chat' ),
    path( 'test', views.chat_test, name='chat_test' ),
]
