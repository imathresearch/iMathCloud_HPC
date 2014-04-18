'''
Created on Dec 18, 2013

@author: iMath
'''

from HPC2.core.jobPlugin import JobPlugin
from HPC2.common.constants import constant
from HPC2.common.util.csvOperations import CSVOperations
from parallelCorrelations import CorrelationParallel
import numpy as np
from HPC2.common.constants import CONS
from butlerCorrelations import ButlerCorrelationParallel

from HPC2.common.util.jobUtils import JobUtils
import os

CONS = CONS()

class JobListPair(JobPlugin):
    
    @constant
    def CORRELATION():
        return "correlation"
    
    @constant
    def BUTLER():
        return "butler"
    
    def __init__(self, jobInfo=None):
        super(JobListPair,self).__init__(jobInfo)
        
    def execute(self):

        function = self.getFunction()
        basicFunc = [self.CORRELATION]
        complexFunc = [self.BUTLER]
        if (function in basicFunc):
            self.__executeBasicFunc(function)
        elif (function in complexFunc):
            self.__executeComplexFunc(function)

    '''
    Functions that can have more than one data file
    '''        
    def __executeComplexFunc(self,function):
        fileStr = str(self.getSourceFile())
        listFiles = fileStr.split(CONS.SEPARATOR)
        result = {
            self.BUTLER: lambda x: self.__startButlerFunction(x)
        }[function](listFiles)
        
        self.setListOutputFiles(result)
        
        mylist = self.getListOutputFiles();
        
    '''
    Functions that only have one data file
    '''        
    def __executeBasicFunc(self,function):
        
        csv = CSVOperations()
        dataMatrix = csv.getDataMatrix(self.getSourceFile())
        # We must transpose the matrix
        aux = np.array(dataMatrix)
        dataMatrix = aux.transpose().tolist()
        
        fileOutput = self.getIdJob() + '_' + function + '.csv'
        
        result = {
            self.CORRELATION: lambda x: self.__startParallelCorrelation(x)
        }[function](dataMatrix)
        
        csv.setDataMatrixToFile(self.getPath(),fileOutput,result)
        
        self.addOutputFile(fileOutput)

        
    def __startParallelCorrelation(self, dataMatrix):
        corrParallel = CorrelationParallel(dataMatrix)
        return corrParallel.startProcess()
    
    
    def __startButlerFunction(self, files):
        csv = CSVOperations()
        datas = []
        for i in range(len(files)):
            fil = files[i]
            dataMatrix = csv.getDataMatrix(fil)
            aux = np.array(dataMatrix) + 1
            #dataMatrix = aux.transpose().tolist()
            datas = datas + [aux]
        
        # We start the parallel execution
        parallel = ButlerCorrelationParallel(datas, self.getIdJob())
        res = parallel.startProcess()
        
        # Now, we must write the files
        fileOutputs = []
        for key in res.iterkeys():
            value = res[key]
            fileName = self.__getFileName(files[key],"NO_NAME")
            fileName = self.__addExtension(fileName, "csv")
            fileOutput =self.getIdJob() + '_out_' + fileName
            fileOutputs = fileOutputs + [fileOutput]
            #print "fileName: ", fileOutput
            csv.setDataMatrixToFile(self.getPath(),fileOutput,value)
        
        return fileOutputs
    
    '''
    Returns solely the file name of the full path parameter
    Example: if fullPath = 'file://media/cloud/files/userName/pepe.aux', it returns 'pepe.aux'
    
    If fullPath is empty, it returns the value of noName
    '''
    def __getFileName(self, fullPath, noName):
        listElems = fullPath.split("/")
        fileName = noName
        if len(listElems)>0:
            fileName = listElems[len(listElems)-1]
        
        return fileName
    
    '''
    Returns the fileName with its extension inly if the it does not end already with the corresponding extension
    
    Example: if fileName = "test.a", and ext = "csv" --> 'test.a.csv'
    Example: if fileName = "test.csv" and ext = "csv", --> 'test.csv'
    Example: if fileName = "" and ext = "csv", --> ".csv"
     
    '''
    def __addExtension(self, fileName, ext):
        outputFile = fileName
        if len(fileName) < len(ext):
            outputFile = outputFile + '.' + ext
        else:
            last = fileName[len(fileName)-len(ext):len(fileName)]   # We get the last len(ext) characters of fileName
            if (last != ext):
                outputFile = outputFile + '.' + ext
    
        return outputFile