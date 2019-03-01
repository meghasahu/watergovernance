from scipy.stats import boxcox
from pandas import Series
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy 

from graphos.sources.csv_file import CSVDataSource
from graphos.sources.simple import SimpleDataSource


#from graphos.renderers.yui import LineChart
from graphos.renderers.gchart import LineChart

from django.shortcuts import render

# monkey patch around bug in ARIMA class
def __getnewargs__(self):
	return ((self.endog),(self.k_lags, self.k_diff, self.k_ma))


def arimaCall(request,modelfile):

	print("in Arima")
	 
	ARIMA.__getnewargs__ = __getnewargs__
	 
	# load data
	series = Series.from_csv('dataset.csv')
	# prepare data
	serial=500
	X = series.values
	X = X.astype('float32')
	# fit model
	model = ARIMA(X, order=(2,1,0))
	model_fit = model.fit(trend='nc', disp=0)
	# bias constant, could be calculated from in-sample mean residual
	bias = 1.081624
	# save model
	model_fit.save('model.pkl')
	numpy.save('model_bias.npy', [bias])

	# load and prepare datasets
	dataset = Series.from_csv('dataset.csv')
	X = dataset.values.astype('float32')
	history = [x for x in X]
	validation = Series.from_csv('validation.csv')
	y = validation.values.astype('float32')
	# load model

	# load model.pkl
	model_fit = ARIMAResults.load(modelfile)
	bias = numpy.load('model_bias.npy')
	# make first prediction
	predictions = list()
	yhat = bias + float(model_fit.forecast()[0])
	yhat = numpy.round(yhat,3)
	predictions.extend(yhat)

	history.append(y[0])
	print('>Predicted=%.3f, Expected=%3.f' % (yhat, y[0]))
	# rolling forecasts
	for i in range(1, len(y)):
		# predict
		model = ARIMA(history, order=(2,1,0))
		model_fit = model.fit(trend='nc', disp=0)
		yhat = bias + float(model_fit.forecast()[0])
		print(type(yhat))
		yhat = numpy.round(yhat,3)
		predictions.extend(yhat)
		# observation
		obs = y[i]
		history.append(obs)
		print('>Predicted=%.3f, Expected=%3.f' % (yhat, obs))
	# report performance
	mse = mean_squared_error(y, predictions)
	rmse = sqrt(mse)
	print('RMSE: %.3f' % rmse)
	#pyplot.plot(y)
	#pyplot.plot(predictions, color='red')
	#pyplot.show()
	

	print(predictions)
	
	data = [['Serial','Y','Prediction']]
	#data.extend(list(zip(predictions,y)))

	sendpred = predictions

	y = list(y)
	sendY = y

	length = len(predictions)
	for i in range(length):
		pred = predictions.pop(0)
		ydata = y.pop(0)
		print(i)
		print(pred)
		print(ydata)
		data.append([serial,ydata,pred])
		serial = serial+50

	print(data)
	
	
	data_source = SimpleDataSource(data=data)

	#chart = LineChart(data_source,options={'title':'Prediction','xaxis':{'mode': "categories"}})
	#chart = LineChart(html_id='gchart_div')
	chart = LineChart(data_source, options={'title': 'Prediction'})

	context = {"chart":chart,"values":data}

	return context