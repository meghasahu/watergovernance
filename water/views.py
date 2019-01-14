from django.shortcuts import render
from django.http import HttpResponse
from water import pyrebase_settings
# Create your views here.
from water.forms import RegisterForm

from water import pyrebase_settings
import pyrebase
# connecting to firebase

#configuration setting 
config = {
    "apiKey": "AIzaSyDJQ46f0iVp_ldrx5Y_AgZ5HWtyI9dfYd8",
    "authDomain": "lbswater.firebaseapp.com",
    "databaseURL": "https://lbswater.firebaseio.com",
    "projectId": "lbswater",
    "storageBucket": "lbswater.appspot.com",
    "messagingSenderId": "1065042380223"
  };

firebase = pyrebase.initialize_app(config);
db = firebase.database()

#Rendering Home Page
def index(request):
	return render(request,'index.html')

# Registeration storing data in firebase
def signup(request):

	if request.method == "POST":
		name = request.POST.get('username')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		address = request.POST.get('address')
		country = request.POST.get('country')
		city = request.POST.get('city')
		state = request.POST.get('state')
		pincode = request.POST.get('pincode')
		password = request.POST.get('password')
		sensor = request.POST.get('sensor')
		#getting db instance
		uniqueid = "1000"+pincode+sensor
		#endid = endid+1
		print(uniqueid)
		print(name)
		print(email)

		data = {"name": name , "email": email,"phoneNo":phone,"address":address,
		"country":country,"city":city,"state":state,"pincode":pincode ,"password":password,"sensorId":sensor}
		db.child("1000").child(uniqueid).set(data)

	return render(request,'sign_up.html')

# signing as admin
def signinadmin(request):

	if request.method == "POST":
		email = request.POST.get('email')
		password = request.POST.get('password')

		val = db.child('1000400074').order_by_child('email').equal_to('2016.megha.sahu@ves.ac.in').get()
		#print(val.order_by_child('password').get())

		
		print(val.val())
		print("hh")

		print("hey")


	return render(request,'sign_in_admin.html')

def signinuser(request):
	return render(request,'sign_in_user.html')

def aboutUs(request):
	return render(request,'about_us.html')

def contact(request):
	return render(request,'contact_us.html')

def adminland(request):
	return render(request,'admin.html')