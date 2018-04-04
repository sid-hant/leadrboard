from django.shortcuts import render, redirect
from . import models
from account import views
from .forms import addPlayerForm, addMatchForm, delPlayerForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Player, Match
from django.views import generic
# Create your views here.

User = get_user_model()

@login_required(login_url='home')
def add(request):
    match_form = addMatchForm()
    player_form = addPlayerForm()
    match_form.fields['p2_name'].queryset = Player.objects.filter(user=request.user)
    match_form.fields['p1_name'].queryset = Player.objects.filter(user=request.user)
    if request.method == 'POST':
        match_form = addMatchForm(request.POST)
        player_form = addPlayerForm(request.POST)
        player_del_form = delPlayerForm(request.POST)
        if match_form.is_valid():
            form = match_form.save(commit=False)
            form.user = request.user
            p1_name = match_form.cleaned_data['p1_name']
            p2_name = match_form.cleaned_data['p2_name']
            p1_score = match_form.cleaned_data['p1_score']
            p2_score = match_form.cleaned_data['p2_score']


            if p1_score > p2_score:
                winner_obj = Player.objects.filter(user=request.user).get(name__iexact=p1_name)
                loser_obj = Player.objects.filter(user=request.user).get(name__iexact=p2_name)
                winner_obj.wins += 1
                print(winner_obj.wins)
                winner_obj.games_played += 1
                loser_obj.loss += 1
                loser_obj.games_played += 1
                winner_obj.save()
                loser_obj.save()
            elif p2_score > p1_score:
                winner_obj = Player.objects.filter(user=request.user).get(name__iexact=p2_name)
                loser_obj = Player.objects.filter(user=request.user).get(name__iexact=p1_name)
                winner_obj.wins += 1
                winner_obj.games_played += 1
                loser_obj.loss += 1
                print(winner_obj.wins)
                loser_obj.games_played += 1
                winner_obj.save()
                loser_obj.save()
            else:
                p1_obj = Player.objects.filter(user=request.user).get(name__iexact=p1_name)
                p2_obj = Player.objects.filter(user=request.user).get(name__iexact=p2_name)
                p1_obj.draw += 1
                p2_obj.draw += 1
                p1_obj.games_played += 1
                p2_obj.games_played += 1
                p1_obj.save()
                p2_obj.save()

            form.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        elif player_form.is_valid():
            form = player_form.save(commit=False)
            form.user = request.user
            form.wins = 0
            form.loss = 0
            form.draw = 0
            form.games_played = 0
            form.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return HttpResponse(reverse('home'))
    return render(request, 'setting.html', {'match_form': match_form, 'player_form':player_form})

class allPlayer(generic.ListView, LoginRequiredMixin):
    login_url = 'home'
    model = models.Player
    template_name = "manage.html"
    context_object_name = "players"
    redirect_field_name = 'home'

    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

class SinglePlayer(generic.DetailView, LoginRequiredMixin):
    model = models.Player
    template_name = 'player_detail.html'
    login_url = 'home'

    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

@login_required(login_url='home')
def Dashboard(request):
    Users = get_user_model()
    players = Player.objects.filter(user=request.user)
    matches = Match.objects.filter(user=request.user)
    user = Users.objects.get(username__iexact=request.user)
    return render(request, 'dashboard.html', {'players': players, 'matches': matches, 'user':user})

class DeletePlayer(generic.DeleteView, LoginRequiredMixin):
    model = models.Player
    success_url = reverse_lazy('home')

@login_required(login_url='home')
def resetPlayer(request, pk):
    obj = Player.objects.get(id=pk)
    obj.wins = 0
    obj.loss = 0
    obj.draw = 0
    obj.games_played = 0
    obj.save()
    return HttpResponseRedirect(reverse_lazy('home'))
