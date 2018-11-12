from django.shortcuts import render

# Create your views here.

def login(request):
	return render(request,'registration/login.html',{})

def signup(request):
	return render(request,'registration/signup.html',{})

