
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),
     path('register/',views.registerUser, name='register'),
    path ('', views.home, name='home'),
    path ('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='createroom'),
    path('update-room/<str:pk>/', views.updateRoom, name='updateroom'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='deleteroom'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='deleteMessage'),
    path ('profile/<str:pk>/', views.userProfile, name='profile'),
    path('update-user/', views.updateUser, name='updateuser'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),



]