from django.shortcuts import render
from django.http import HttpResponse
from water import pyrebase_settings
# Create your views here.


def index(request):
	return render(request,'index.html')

def signup(request):
	return render(request,'sign_up.html')

def signinadmin(request):
	return render(request,'sign_in_admin.html')

def signinuser(request):
	return render(request,'sign_in_user.html')

def aboutUs(request):
	return render(request,'about_us.html')

def contact(request):
	return render(request,'contact_us.html')

def adminland(request):
	return render(request,'admin.html')