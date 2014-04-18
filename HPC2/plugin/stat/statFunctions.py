import numpy as np
from scipy import stats

class StatisticalFunction:

	def StatMean(self,data):
		
		dataNp = np.array(data)
		meanVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			DataColumn = dataNp[:,i]
			meanVector.append(np.mean(DataColumn))
		return meanVector
		
	def Frecuency(self,data):
		dataNp = np.array(data)
		Frecuencies = []
		lengthColumns = len(data)
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			x = []
			lengthRows = len(dataNp[0])
			rangeRows = range(lengthRows)
			for j in rangeRows:
				element = dataNp[i,j]
				x.append(element)
			y = np.bincount(x)
			ii = np.nonzero(y)[0]
			Frecuencies.append(zip(ii,y[ii]))
		return Frecuencies
		
	def Probabilies(self,Frecuencies):
		dataNp = np.array(Frecuencies)
		Probabilities = []
		for element in dataNp:
			ActualProbability = []
			npArrayFrecuency = element[1]
			SumFrecuencies = np.sum(npArrayFrecuency)
			ActualProbability.append(element[0])
			ActualProbability.append(element[1] / SumFrecuencies)
			Probabilities.append(ActualProbability)
		return Probabilities

	def StatStd(self,data):
		dataNp = np.array(data)
		StdVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			DataColumn = dataNp[:,i]
			StdVector.append(np.std(DataColumn))
		return StdVector
		
	def StatVar(self,data):
		dataNp = np.array(data)
		VarVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			DataColumn = dataNp[:,i]
			VarVector.append(np.std(DataColumn) * np.std(DataColumn))
		return VarVector
		
	def StatMax(self,data):
		dataNp = np.array(data)
		MaxVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			DataColumn = dataNp[:,i]
			MaxVector.append(np.amax(DataColumn))
		return MaxVector
		
	def StatMin(self,data):
		dataNp = np.array(data)
		MinVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			DataColumn = dataNp[:,i]
			MinVector.append(np.amin(DataColumn))
		return MinVector
		
	def StatMedian(self,data):
		dataNp = np.array(data)
		MedianVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			DataColumn = dataNp[:,i]
			MedianVector.append(np.median(DataColumn))
		return MedianVector
		
	def StatPercentile(self,data,per):
		per = per if isinstance(per, list) else [per]
		dataNp = np.array(data)
		PercentileVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			DataColumn = dataNp[:,i]
			ResultPercentile = [stats.scoreatpercentile(DataColumn,float(peri)) for peri in per]
			PercentileVector.append(ResultPercentile)
		return PercentileVector
		
	def StatMode(self,data):
		dataNp = np.array(data)
		ModeVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			DataColumn = dataNp[:,i]
			ActualValue = stats.mode(DataColumn)
			ModeVector.append(ActualValue)
		return ModeVector
		
	def StatLinearRegression(self,data):
		dataNp = np.array(data)
		LinearRegressionVector = []
		lengthColumns = len(dataNp[0])
		rangeLength = range(lengthColumns)
		for i in rangeLength:
			for j in rangeLength:
				if (i!=j):
					DataColumn = [dataNp[:,i],dataNp[:,j]]
					ResultsLinearRegression = stats.linregress(DataColumn)
					LinearRegressionVector.append(ResultsLinearRegression)
		return LinearRegressionVector
		
	def StatLinearRegressionPrevision(self,data,Value):
		FieldsLinearRegression = self.StatLinearRegression(data)
		PredictionValueVector = []
		for ActualFieldsLinearRegression in FieldsLinearRegression:
			slope = ActualFieldsLinearRegression[0]
			PercentaleSlope = float(slope) * float(Value)
			bias = ActualFieldsLinearRegression[1]
			Prediction = PercentaleSlope + float(bias)
			PredictionValueVector.append(Prediction)
		return PredictionValueVector
