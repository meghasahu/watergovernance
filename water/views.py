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
import pandas
from pandas import Series
import io

# installed pillow but for old compatibility they use PIL only
import PIL
import PIL.Image

import base64

import water.arima as arima
import water.modelTest as modelTest
import water.cleanData as cleanData
from graphos.renderers.yui import LineChart

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('lbswater-firebase-adminsdk-en8mh-fe88f0158d.json')
firebase = firebase_admin.initialize_app(cred,{'databaseURL': 'https://lbswater.firebaseio.com/'});

ref = db.reference()

# connecting to firebase

#configuration setting 
"""config = {
    "apiKey": "AIzaSyDJQ46f0iVp_ldrx5Y_AgZ5HWtyI9dfYd8",
    "authDomain": "lbswater.firebaseapp.com",
    "databaseURL": "https://lbswater.firebaseio.com",
    "projectId": "lbswater",
    "storageBucket": "lbswater.appspot.com",
    "messagingSenderId": "1065042380223"
  };

firebase = pyrebase.initialize_app(config);
db = firebase.database()"""

#Rendering Home Page
def index(request):
	return render(request,'index.html')


def aboutUs(request):

	return render(request,'about.html')



def contact(request):
	return render(request,'contact.html')

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
		ref.child("1000").child(uniqueid).set(data)
		request.session['username'] = email

		return render(request,'user.html')
	else:
		return render(request,'signup.html')

# signing as admin
def signinadmin(request):

	if request.method == "POST":
		email = request.POST.get('email')
		password = request.POST.get('password')

		#val = db.child('1000400074').order_by_child('email').equal_to('2016.megha.sahu@ves.ac.in').get()
		#print(val.order_by_child('password').get())

		# fetching data where email id is equals to email
		val = ref.child('admin').order_by_child("email").equal_to(email).get()
		print("in")

		#print(val.val())
		
		# accessing fetched data 
		for key,value in val.items():
			print("hey")

			# getting value from pyrebase object

			print(value["password"])

			# comparing fetched password and entered password
			if(value["password"] == password):
				print("rendering")
				request.session['adminname'] = email
				return render(request,'admin.html')

			else:
				messages.warning(request,"Login Failed")
				return render(request,'adminpanel.html')


	return render(request,'adminpanel.html')

#signing in as user
def signin_user(request):

	if request.method == "POST":
		email = request.POST.get('username')
		password = request.POST.get('password')
		print(email)

		#val = db.child('1000400074').order_by_child('email').equal_to('2016.megha.sahu@ves.ac.in').get()
		#print(val.order_by_child('password').get())

		# fetching data where email id is equals to email
		val = ref.child('1000').order_by_child('email').equal_to(email).get()
		print("email")
		print(val)
		# accessing fetched data 
		for key,value in val.items():
			# getting value from pyrebase object
			#for val2 in val1:
			print("password")
			print(value)
			#print(val2[1])

			# comparing fetched password and entered password
			if(value["password"] == password):
				print("rendering")
				request.session['username'] = email
				#messages.success(request,"Login successful")
				return render(request,'user.html')

			else:
				messages.warning(request,"Login Failed")
				return render(request,'publicpanel.html')

	return render(request,'publicpanel.html')

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
			keys= []

			# fetching data from start date to end date
			#val = db.child('consumption').order_by_child('date').equal_to('13-01-2019').get()

			#fetching all the users in consumption
			val = ref.child('1000').get()

			for allkey in val.each():
				keys.append(allkey.key())
				print(keys)

			for key in keys:
				print(key)
				val = ref.child('consumption').child(key).order_by_child('date').start_at(startdate).end_at(enddate).get()
				for vals in val.each():
					v = vals.val()
					data.append([v['date'],v['consumed']])
					#data.append([])
					print("printing v")
					print(data)
			
			# creating csv file and saving fetched data into it
			with open('new.csv','w',newline='') as file1:
				writer = csv.writer(file1)
				writer.writerows(data)

		return render(request,'admin.html')

	else:
		return render(request,'sign_in_admin.html')

def cleanDataset(request):
	if request.session.has_key('adminname'):
		if request.method == "POST":
			file1 = request.POST.get("fileupload")
			cleanData.cleanData(request,file1)
		return render(request, 'uploadDataset.html')
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

			ref.child("admin").push(data)
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


def admin_logout(request):
	try:
		del request.session['adminname']
	except:
		pass
	return render(request,'index.html')

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

def user_alerts(request):
	if request.session.has_key('username'):

		return render(request,'user_alerts.html')
	else:
		return render(request,'sign_in_user.html')





def modelResult(request):

	print("in")

	series = Series.from_csv('water.csv', header=0)
	split_point = len(series) - 10
	dataset, validation = series[0:split_point], series[split_point:]
	print('Dataset %d, Validation %d' % (len(dataset), len(validation)))
	dataset.to_csv('dataset.csv')
	validation.to_csv('validation.csv')

	# load data
	series = Series.from_csv('dataset.csv')
	# prepare data
	X = series.values
	X = X.astype('float32')
	train_size = int(len(X) * 0.50)
	train, test = X[0:train_size], X[train_size:]
	# walk-forward validation
	history = [x for x in train]
	predictions = list()
	for i in range(len(test)):
		# predict
		yhat = history[-1]
		predictions.append(yhat)
		# observation
		obs = test[i]
		history.append(obs)
		print('>Predicted=%.3f, Expected=%3.f' % (yhat, obs))
	# report performance
	mse = mean_squared_error(test, predictions)
	rmse = sqrt(mse)
	print('RMSE: %.3f' % rmse)

	fig = Figure()
	ax = fig.add_subplot(111)
	data_df = pandas.read_csv("dataset.csv")
	data_df = pandas.DataFrame(data_df)
	data_df.plot(ax=ax)
	canvas = FigureCanvas(fig)
	fig.savefig('water/static/img/test.png')
	response = HttpResponse( content_type = 'image/png')
	canvas.print_png(response)


	#return response

	"""
	series = Series.from_csv('dataset.csv')
	res = series.plot()
	#pyplot.show()

	print("hey")

	
	buffer = io.BytesIO()
	canvas = pyplot.get_current_fig_manager().canvas
	canvas.draw()
	#graphIMG = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())

	graphIMG = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
	graphIMG.save(buffer,"PNG")
	pyplot.close()
	graph = base64.b64encode(buffer.getvalue())

	"""
	#return response

    #return HttpResponse(buffer.getvalue(), content_type="image/png")

	return render(request,'modelResult.html')

def admin_logout(request):
	try:
		del request.session['username']
	except:
		pass
	return render(request,'index.html')

def user_logout(request):

	try:
		del request.session['username']
	except:
		pass
	return render(request,'index.html')
