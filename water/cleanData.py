from pandas import Series
from shutil import copyfile

def cleanData(request,file1):
	series = Series.from_csv(file1, header=0)
	split_point = len(series) - 10
	dataset, validation = series[0:split_point], series[split_point:]
	print('Dataset %d, Validation %d' % (len(dataset), len(validation)))

	dataset.to_csv('dataset.csv')
	validation.to_csv('validation.csv')

	copyfile("dataset.csv","C:\\Users\\ankur\\Desktop\\data.csv")
	copyfile("validation.csv","C:\\Users\\ankur\\Desktop\\valid.csv")

	return