from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Game
from .forms import NewGameForm
from django.views.generic.edit import CreateView

def home(request):
	#import pdb; pdb.set_trace()
	context = {
		'posts': Post.objects.all()
		#'posts': posts
	}
	return render(request, 'App/home.html', context)

def account(request):
	return render(request, 'Users/profile.html')

def dashboard(request):
	return render(request, 'dashboard.html')

def help(request):
	return render(request, 'Help.html')

def login(request):
	return render(request, 'Login.html')

def lobby(request):
    #import pdb; pdb.set_trace()
    context = {
        'games': Game.objects.all()
        #'posts': posts
    }
    return render(request, 'App/lobby.html', context)

@login_required
def new_game(request):
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.host = request.user
            f.save()
            #game_name = form.cleaned_data.get('game_name')
            messages.success(request, f'New Game created!')
            return redirect('app-lobby')
    else:
        form = NewGameForm(instance=request.user)
    #import pdb; pdb.set_trace()
    return render(request, 'App/new_game.html', {'form': form})

@login_required
def joinGame(request):
    return render(request, 'App/join_game.html')
    """if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.host = request.user
            f.save()
            #game_name = form.cleaned_data.get('game_name')
            messages.success(request, f'New Game created!')
            return redirect('app-lobby')
    else:
        form = NewGameForm(instance=request.user)
    #import pdb; pdb.set_trace()
    return render(request, 'App/new_game.html', {'form': form})"""
