from django.urls import path
from .views import SignUpView,SignUpdoneView,Login,HomeView,Logout, TopView,room, room_test
#from .views import Login,Logout,HomeView,TopView,SignUpView,SignUpdoneView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup_done/', SignUpdoneView.as_view(), name='signup_done'),
    path('login/', Login.as_view(), name='login'),
    path('profile/', HomeView.as_view(), name='profile'),
    path('logout/', Logout.as_view(), name='logout'),
    path('top/', TopView.as_view(), name='top'),
    # #path('room/<int:pk>/', room, name='room'),
    path('room/<str:pk>/', room, name='room'),
    path('room_test/<str:pk>', room_test, name='room_test'),

]