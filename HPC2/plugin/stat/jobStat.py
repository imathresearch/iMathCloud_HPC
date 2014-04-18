'''
Created on 12/12/2013

@author: iMath
'''
import os
from HPC2.core.jobPlugin import JobPlugin
from HPC2.common.constants import constant
from statFunctions import StatisticalFunction
from HPC2.common.util.csvOperations import CSVOperations
import urlparse as up
import numpy as np
from plotFunctions import Plots
from HPC2.common.util.json import JSON

from HPC2.common.util.jobUtils import JobUtils

class JobStat(JobPlugin):
    
    @constant
    def DESCSTAT():
        return "DescriptiveStatistics"
    
    @constant
    def MEAN():
        return "Mean"
    
    @constant
    def FREQ():
        return "Frecuencies"
    
    @constant
    def STDEV():
        return "StandardDeviation"
    
    @constant
    def VAR():
        return "Variance"
    
    @constant
    def MAX():
        return "Maximum"
    
    @constant
    def MIN():
        return "Minimum"
    
    @constant
    def MEDIAN():
        return "Median"
    
    @constant
    def MODE():
        return "Mode"
    
    @constant
    def LINREG():
        return "LinearRegression"
    
    @constant
    def LINREGPREV():
        return "LinearRegressionPrevision"
    
    @constant
    def PLOTDESC():
        return "PlotDescStat"
    
    @constant
    def PLOTLINREG():
        return "PlotLinReg"
    
    
    def __init__(self, jobInfo=None):
        super(JobStat,self).__init__(jobInfo)
        
    def execute(self):

        function = self.getFunction()
        #print function
        basicFunc = [self.MEAN, self.FREQ, self.STDEV, self.VAR, self.MAX, self.MIN, self.MODE, self.MEDIAN, self.LINREG]
        paramFunc = [self.LINREGPREV, self.DESCSTAT]
        plotFunc = [self.PLOTDESC, self.PLOTLINREG]
        if function in basicFunc:
            self.__execBasicFunc(function)
        elif function in plotFunc:
            self.__execPlotFunc(function)
    
    
    def __execPlotFunc(self,function):
        csv = CSVOperations()
        dataMatrix = csv.getDataMatrix(self.getSourceFile())
        fileOutput = self.getIdJob() + '_' + function + '.svg'
        aux = up.urlparse(self.getPath())
        path = aux.path
        fileOutPath = path + '/' + fileOutput
        {
            self.PLOTDESC: lambda x,y: self.__plotDesc(x,y),
            self.PLOTLINREG: lambda x,y: self.__plotLinReg(x,y)        
        }[function](dataMatrix, fileOutPath)
        
        self.addOutputFile(fileOutput)
    
    
    def __plotDesc(self, dataMatrix, fileOutPath):
        data = np.array(dataMatrix)
        nVars = len(data[0])
        nObs = len(data)
        classPlot = Plots()
        if (nVars>1):
            classPlot.MultivarDescStat(data,fileOutPath)
        else:
            classPlot.UnivarDescStat(data,fileOutPath)    
 
    def __plotLinReg(self, dataMatrix, fileOutPath):
        myJSON = JSON()
        parameter = myJSON.JSonStringToJsonEncoder(self.getParameter())
        data = np.array(dataMatrix)[:,parameter['columns']]
        classPlot = Plots()
        classPlot.PolinomialRegression(data,fileOutPath,parameter['hasHeader'],parameter['polinomialDegree'])

    def __execBasicFunc(self,function):
        
        classStat = StatisticalFunction()
        csv = CSVOperations()
        dataMatrix = csv.getDataMatrix(self.getSourceFile())
        fileOutput = self.getIdJob() + '_' + function + '.csv'
        result = {
            self.MEAN: lambda x: classStat.StatMean(x),
            self.FREQ: lambda x: classStat.Frecuency(x),
            self.STDEV: lambda x: classStat.StatStd(x),
            self.VAR: lambda x: classStat.StatVar(x),
            self.MAX: lambda x: classStat.StatMax(x) ,
            self.MIN: lambda x: classStat.StatMin(x) ,
            self.MODE: lambda x: classStat.StatMode(x),
            self.MEDIAN: lambda x: classStat.StatMedian(x),
            self.LINREG: lambda x: classStat.StatLinearRegression(x),
        }[function](dataMatrix)
        csv.setDataMatrixToFile(self.getPath(),fileOutput,result)
    
        self.addOutputFile(fileOutput)
    
          