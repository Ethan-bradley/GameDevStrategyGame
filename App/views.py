from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request, 'Home.html')

def account_info(request):
	return render(request, 'AccountInfo.html')

def dashboard(request):
	return render(request, 'dashboard.html')

def help(request):
	return render(request, 'Help.html')

def login(request):
	return render(request, 'Login.html')
