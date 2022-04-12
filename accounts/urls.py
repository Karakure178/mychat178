from django.urls import path
from .views import SignUpView,SignUpdoneView,Login,HomeView,Logout, TopView,room, room_test,RoomAddView,ChatTestView,UserChangeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup_done/', SignUpdoneView.as_view(), name='signup_done'),
    path('login/', Login.as_view(), name='login'),
    path('profile/', HomeView.as_view(), name='profile'),
    path('profile_edit/', UserChangeView.as_view(), name='profile_edit'),


    path('logout/', Logout.as_view(), name='logout'),
    path('top/', TopView.as_view(), name='top'),
    # #path('room/<int:pk>/', room, name='room'),
    path('room/<str:pk>/', room, name='room'),
    path('room_test/<str:pk>', room_test, name='room_test'),
    
    path( 'test', ChatTestView.as_view(), name='chat_test' ),
    path('room_add/', RoomAddView.as_view(), name='room_add'),

]





#from django.urls import path
#from .views import HomeView, TestView,UserChangeView
#from . import views

#urlpatterns = [
    #path( '', views.chat, name='chat' ),
    #path( 'test', views.chat_test, name='chat_test' ),
    #path('home/', HomeView.as_view(), name='home'),
#]
