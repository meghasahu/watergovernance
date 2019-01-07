from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
	return render(request,'index.html')

def signup(request):
	return render(request,'sign_up.html')