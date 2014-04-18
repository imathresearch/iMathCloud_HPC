import csv
from urlparse import urlparse
import numpy as np

class CSVOperations:

	def openCSVFile(self,FilePath,Type):
		FileOpened = open(FilePath,Type)
		return FileOpened
		
	def readCSVFile(self,File,delimiterUser):
		Data = File.readlines()
		CSVRead = Data
		return CSVRead
		
	def crossedFile(self,CSVFile):
		Data = []
		for row in CSVFile:
			DataRow = []
			StringValue = ''
			for character in row:
				if character==',':
					DataRow.append(float(StringValue))
					StringValue = ''
				else:
					StringValue += character
			DataRow.append(float(StringValue))
			Data.append(DataRow)
		return Data
		
	def writeDataFile(self,fil,data):
		#TODO: error controls: What happens if we have more than 2 dimensions in the data?????
		npData = np.array(data)
		dim= npData.shape
		
		if (len(dim)==1):
			self.__writeCSVLine(fil, str(data))
		elif (len(dim)==2):
			x = dim[0]
			for i in range(x):
				linData=data[i]
				if(i>0):
					self.__writeLn(fil)
				self.__writeCSVLine(fil, str(linData))
		else:
			self.__writeCSVLine(fil, str(data))
		
		return 0
	
	def __writeLn(self,fil):
		fil.write("\n")
		
	def __writeCSVLine(self, fil, line):
		line = line[1:len(line)-1]
		#print line
		csvValue = ''
		for character in line:
			if character!=' ':
				csvValue = csvValue + character
		fil.write(csvValue)
		
	def closeCSVFile(self,File):
		File.close()
		return 0
	
	def getDataMatrix(self,FilenamePath):
		
		aux = urlparse(FilenamePath)
		FilenamePath = aux.path
		csvFileOpen = self.openCSVFile(FilenamePath,'rb')
		readCSVFile = self.readCSVFile(csvFileOpen,',')
		dataMatrix = self.crossedFile(readCSVFile)
		self.closeCSVFile(csvFileOpen)
		return dataMatrix

	def setDataMatrixToFile(self,Directory,FileOutput,result):
		
		Directory = urlparse(Directory).path
		PathOutputFile = Directory + '/' + FileOutput
		csvFileOutput = self.openCSVFile(PathOutputFile,'w')
		ResultFileOutput = self.writeDataFile(csvFileOutput,result)
		self.closeCSVFile(csvFileOutput)
		return 0
