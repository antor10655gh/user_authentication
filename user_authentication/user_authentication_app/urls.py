from django.conf.urls import url
from django.urls import path
from user_authentication_app import views

app_name = "user_authentication_app"

urlpatterns = [
     path('index/', views.index, name='index'),
]
