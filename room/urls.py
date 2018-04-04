from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'room'

urlpatterns = [
    path('add/', views.add, name='add'),
    path('manage/', login_required(views.allPlayer.as_view(), login_url='home'), name='manage'),
    path('manage/<pk>/', login_required(views.SinglePlayer.as_view()), name='player_detail'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('manage/delete/<pk>', login_required(views.DeletePlayer.as_view(), login_url='home'), name='delete_player'),
    path('manage/reset/<pk>', views.resetPlayer, name='reset_player')
]
