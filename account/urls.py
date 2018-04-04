from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'account'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view() , name='logout'),
    path('login/', views.user_login, name='login'),
    path('search/', views.search_for_room, name='search'),
    path('room/<pk>', views.userDetail, name='user_detail')
]
