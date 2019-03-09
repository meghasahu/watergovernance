from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import json
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
import xlwt

# installed pillow but for old compatibility they use PIL only

import base64
import water.arima as arima
import water.modelTest as modelTest
import water.cleanData as cleanData
from graphos.renderers.gchart import LineChart

# for consumption display converting consumption to json
import datetime
from graphos.renderers.gchart import GaugeChart

import firebase_admin                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('lbswater-firebase-adminsdk-en8mh-fe88f0158d.json')
firebase = firebase_admin.initialize_app(cred,{'databaseURL': 'https://lbswater.firebaseio.com/'});

ref = db.reference()

# connecting to firebase


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
		smartid = request.POST.get('smartid')
		members = request.POST.get('members')
		#city = request.POST.get('city')
		#state = request.POST.get('state')
		#pincode = request.POST.get('pincode')
		password = request.POST.get('password')
		sensor = request.POST.get('sensor')
		#getting db instance
		uniqueid = "1000"+smartid+sensor
		#endid = endid+1
		print(uniqueid)
		print(name)
		print(email)

		data = {"name": name , "email": email,"phoneNo":phone,"address":address,"smartid":smartid ,"password":password,"sensorId":sensor,"members":members}
		ref.child("1000").child(uniqueid).set(data)
		request.session['username'] = uniqueid

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

		#print(val.val())
		
		# accessing fetched data 
		for key,value in val.items():
			print("hey")

			# getting value from pyrebase object

			print(value["password"])

			# comparing fetched password and entered password
			if(value["password"] == password):
				print("rendering")
				request.session['adminname'] = key
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
				request.session['username'] = key
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

			print(startdate)
			print(enddate)
			keys= []
			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename="users.xls"'

			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('Users')

			row_num = 0
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			csvdata = list()

			# fetching data from start date to end date
			#val = db.child('consumption').order_by_child('date').equal_to('13-01-2019').get()

			#fetching all the users in consumption
			val = ref.child('1000').get()

			for allkey,data in val.items():
				keys.append(allkey)
				print(keys)
			'''for col_num in range(len(columns)):
        		ws.write(row_num, col_num, columns[col_num], font_style)'''

    		# Sheet body, remaining rows

			for key in keys:
				print(key)
				val = ref.child('water_consumption').child(key).order_by_child('date').start_at('2019-02-01').end_at('2019-02-02').get()
				val = ref.child('water_consumption').child(key).order_by_child('date').equal_to('2019-02-01').get()
				print(val)
				
				for key,v in val.items():
					csvdata.append([v['date'],v['consumed']])
					#data.append([])
					print("printing v")
					print(csvdata)
			"""font_style = xlwt.XFStyle()
			for row in columns:
				row_num += 1
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)"""

			print("hello")
			
			# creating csv file and saving fetched data into it
			with open('new.csv','w',newline='') as file1:
				writer = csv.writer(file1)
				writer.writerows(csvdata)

			with open('new.csv', 'rb') as myfile:
				response = HttpResponse(myfile, content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename=new.csv'
            
        	#return HttpResponse(response,content_type='application/csv')

			#return HttpResponse(response,content_type='application/csv')
			return response
		else:
			return render(request,'admin.html',{})

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
		data = 0
		date = str(datetime.datetime.now().date())
		print(date)
		userid = request.session.get('username')

		# getting consumption of the day
		consumption = ref.child('water_consumption').child(userid).order_by_child('date').equal_to(date).get()
		print(consumption)
		for key,val in consumption.items():
			print(val)
			data = val["consumed"]

		info = ref.child('1000').child(userid).get()
		print(info)
		
		members = info["members"]

		allowed = members*50

		return render(request,'user.html',{'myconsumption':data,'members':members,'allowed':allowed})
	else:
		return render(request,'sign_in_user.html')

def user_alerts(request):
	if request.session.has_key('username'):
		Alerts1=list()
		table=['Date','Consumed']
		alertlist = ref.child('alerts').child(request.session.get('username')).get();
		
		for key,value in alertlist.items():
			Alerts1.append(value)

			table.append([value["date"],value["consumed"],])

			print(Alerts1)
		
		
		print(table)

		userid = request.session.get('username')
		val = ref.child('alerts').child(userid).order_by_child('date').get()
		table=list()
		for key,value in val.items():
			#data.append([i,value["consumed"],expected])

			table.append([value["date"],value["consumed"]])
			#i=i+1


		return render(request,'user_alerts.html',{'table':table})
	else:
		return render(request,'sign_in_user.html')


"""
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

	
	#return response

    #return HttpResponse(buffer.getvalue(), content_type="image/png")

	return render(request,'modelResult.html')
"""
def user_month(request):

	userid = request.session.get('username')
	val = ref.child('water_consumption').child(userid).order_by_child('date').limit_to_first(30).get()

	data = [['Serial','Consumed','Threshold']]
	table=list()
	i = 0
	info = ref.child('1000').child(userid).get()
	print(info)
	
	members = info["members"]

	allowed = members*50
	for key,value in val.items():
		data.append([i,value["consumed"],allowed])

		table.append([value["date"],value["consumed"]])
		i=i+1
	
	data_source = SimpleDataSource(data=data)
	chart = LineChart(data_source, options={'title': 'Monthly Statistics'})
	print(table)
	#context = {"chart":chart,"values":data}
	return render(request,'user_month.html',{'chart':chart,'table':table,'members':members})
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
