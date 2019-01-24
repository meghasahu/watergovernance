from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
from django.contrib import messages
import csv

from graphos.sources.simple import SimpleDataSource

#Package for model

from statsmodels.tsa.arima_model import ARIMA,ARIMAResults
from scipy.stats import boxcox
import numpy
from sklearn.metrics import mean_squared_error
from math import sqrt

from matplotlib import pyplot

import pandas
from pandas import Series

from matplotlib import pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import io

# installed pillow but for old compatibility they use PIL only
import PIL
import PIL.Image

import base64

import water.arima as arima
import water.modelTest as modelTest
from graphos.renderers.yui import LineChart

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


def aboutUs(request):
	print("HIII")
	return render(request,'about_us.html')

def contact(request):
	return render(request,'contact_us.html')

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

		#val = db.child('1000400074').order_by_child('email').equal_to('2016.megha.sahu@ves.ac.in').get()
		#print(val.order_by_child('password').get())

		# fetching data where email id is equals to email
		val = db.child('admin').order_by_child('email').equal_to(email).get()
		print("in")

		#print(val.val())
		
		# accessing fetched data 
		for val1 in val.each():
			print("hey")

			# getting value from pyrebase object
			value = val1.val()

			print(value["password"])

			# comparing fetched password and entered password
			if(value["password"] == password):
				print("rendering")
				request.session['adminname'] = email
				return render(request,'admin.html')

			else:
				messages.warning(request,"Login Failed")
				return render(request,'sign_in_admin.html')


	return render(request,'sign_in_admin.html')

#signing in as user
def signin_user(request):

	if request.method == "POST":
		email = request.POST.get('username')
		password = request.POST.get('password')

		#val = db.child('1000400074').order_by_child('email').equal_to('2016.megha.sahu@ves.ac.in').get()
		#print(val.order_by_child('password').get())

		# fetching data where email id is equals to email
		val = db.child('1000').order_by_child('email').equal_to(email).get()
		
		# accessing fetched data 
		for val1 in val.each():

			# getting value from pyrebase object
			value = val1.val()

			print(value["password"])

			# comparing fetched password and entered password
			if(value["password"] == password):
				print("rendering")
				request.session['username'] = email
				messages.success(request,"Login successful")
				return render(request,'user.html')

			else:
				messages.warning(request,"Login Failed")
				return render(request,'sign_in_user.html')

	return render(request,'sign_in_user.html')

# Admin Functions

def getfile(request):  
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="file.csv"'  
    writer = csv.writer(response)  
    writer.writerow(['1001', 'John', 'Domil', 'CA'])  
    writer.writerow(['1002', 'Amit', 'Mukharji', 'LA', '"Testing"'])  
    return response  


def adminland(request):

	if request.session.has_key('adminname'):

		if request.method == "POST":
			startdate = request.POST.get('startingyear')
			enddate = request.POST.get('endingyear')

			data = list()

			print(startdate)
			print(enddate)

			# fetching data from start date to end date
			#val = db.child('consumption').order_by_child('date').equal_to('13-01-2019').get()

			val = db.child('consumption').get().val()


			print(val.key())

			"""
			for vibe_dict in val.items(): # dict is a Python keyword, so it's a bad choice for a variable!
				print(vibe_dict[0])
				result = db.child('consumption').child(vibe_dict[0]).order_by_child('date').equal_to('13-01-2019').get().val()

				for consumption in val.each():
					v = consumption.val()
					data.append([v])
					print("printing v")
					print(data)

			
			#start_at('13-01-2019').end_at('14-01-2019')

			
			

			
			# creating csv file and saving fetched data into it
			with open('new.csv','w',newline='') as file1:
				writer = csv.writer(file1)
				writer.writerows(data)

			print(val)
			"""	

			getfile()
			#return render(request,'modelResult.html')
		else:
			return render(request,'admin.html')

	else:
		return render(request,'sign_in_admin.html')

def uploadModel(request):
	if request.session.has_key('adminname'):
		return render(request, 'uploadModel.html')
	else:
		return render(request,'sign_in_admin.html')



def modelResult(request):

	if request.session.has_key('adminname'):

		if request.method == "POST":

			modelFile = request.POST.get("fileupload")
			content = arima.arimaCall(request,modelFile)
			return render(request, 'table.html', content)
	else:
		return render(request,'sign_in_admin.html')

def getModel(request):

	if request.session.has_key('adminname'):

		if request.method == "POST":

			print("getting")

			file = request.POST.get("fileupload")

			modelTest.modelT(request,file)

			message = "Your Model has been successfully Trained for the dataset"
			return render(request,'getModel.html',{"msg":message})
		else:
			message = " "
			return render(request,'getModel.html',{"msg":message})

	else:
		return render(request,'sign_in_admin.html')

def addAdmin(request):
	if request.session.has_key('adminname'):
		if request.method == "POST":
			email = request.POST.get("email")
			name = request.POST.get("name")
			phone = request.POST.get("phone")
			password = request.POST.get("password")

			data = {"email":email,"name":name,"phone":phone,"password":password}

			db.child("admin").push(data)
			return render(request,'add_admin.html')

		else:
			return render(request,'add_admin.html')

	else:
		return render(request,'sign_in_admin.html')

def adminAlerts(request):
	if request.session.has_key('adminname'):


		return render(request,'admin_alerts.html')

	else:
		return render(request,'sign_in_admin.html')

def userInfo(request):
	if request.session.has_key('adminname'):


		return render(request,'check_user.html')

	else:
		return render(request,'sign_in_admin.html')


# User Functions

def userland(request):
	if request.session.has_key('username'):
		return render(request,'user.html')

	else:
		return render(request,'sign_in_user.html')

def admin_logout(request):
	try:
		del request.session['adminname']
	except:
		pass
	return render(request,'index.html')