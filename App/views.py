from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request, 'App/home.html')

def account(request):
	return render(request, 'Users/profile.html')

def dashboard(request):
	return render(request, 'dashboard.html')

def help(request):
	return render(request, 'Help.html')

def login(request):
	return render(request, 'Login.html')
