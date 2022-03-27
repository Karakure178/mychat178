from django.shortcuts import render

# Create your views here.

def chat( request ):
    return render( request, 'chat/chat.html' )

def chat_test( request ):
    return render( request, 'chat/chat_test.html' )