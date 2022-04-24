from django.urls import path
from .views import SignUpView,SignUpdoneView,Login,HomeView,Logout, TopView,RoomAddView,ChatTestView,UserChangeView,TestView,GreetView
from .views import ChatViewSet,RoomViewSet
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup_done/', SignUpdoneView.as_view(), name='signup_done'),
    path('login/', Login.as_view(), name='login'),
    path('profile/', HomeView.as_view(), name='profile'),
    path('profile_edit/', UserChangeView.as_view(), name='profile_edit'),


    path('logout/', Logout.as_view(), name='logout'),
    path('top/', TopView.as_view(), name='top'),
        
    path( 'test', ChatTestView.as_view(), name='chat_test' ),
    path('room_add/', RoomAddView.as_view(), name='room_add'),

    path("c_test",TestView.as_view(),name="test"),

    path('api_chat/', ChatViewSet.as_view(), name='detail'),
    path('api_chat/<str:room>/', ChatViewSet.as_view(), name='detail'),
    path('api_room/<int:meta>/', RoomViewSet.as_view(), name='detail'),

    path('ajax_test/', GreetView.as_view(), name='ajax_test'),
]
