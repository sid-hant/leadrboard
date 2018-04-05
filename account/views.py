from django.shortcuts import render
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model
from django.views import generic
from room.models import Player, Match


# Create your views here.
def user_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('room:dashboard'))
    elif request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        user_form = forms.UserForm()
    return render(request,'home.html',{'user_form':user_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        return render(request, 'home.html')

def search_for_room(request):
    Users = get_user_model()
    if request.method == 'GET':
        room_name = request.GET.get('search')
        rooms = Users.objects.filter(username__icontains=room_name)
        return render(request,"search.html",{"rooms":rooms})
    else:
        return render(request,"search.html",{})

def userDetail(request, pk):
    Users = get_user_model()
    user = Users.objects.get(id=pk)
    name = user.username
    players = Player.objects.filter(user=user)
    matches = Match.objects.filter(user=user)
    return render(request,"user_detail.html",{'players':players, 'matches':matches, 'name':name})
