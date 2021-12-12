from django.conf.urls import url
from django.urls import path
from user_authentication_app import views

app_name = "user_authentication_app"

urlpatterns = [
     path('', views.index, name='index'),
     path('register/', views.register, name='register'),
     path('log_in/', views.log_in, name='log_in'),
     path('user_login/', views.user_login, name='user_login'),
     path('user_logout/', views.user_logout, name='user_logout'),
]
