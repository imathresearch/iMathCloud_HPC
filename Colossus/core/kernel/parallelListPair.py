'''
Created on 27/12/2013

@author: iMath
'''
import abc
import pickle

from Colossus.exception.exceptions import ColossusException
import Colossus.core.kernel.parallel_gen



class ParallelListPairExtended(Colossus.core.kernel.parallel_gen.ParallelGen):
    '''
    The same as ParallelListPair, but considering multiple data tables
    '''
    __metaclass__ = abc.ABCMeta
    
    sizeDatas = []      # The number of elems for each data table
    sizeDatasPair = []      # The number of pair elems for each data table
    totalElements = 0       # The total number of pair elements
    
    def __init__(self, datas, idJob = None):
        
        self.data=datas
        self.idJob = idJob
        self.__computeSizes(datas)
        
    def __computeSizes(self,datas):
        self.sizeDatas = [0 for _ in range(len(datas))]
        self.sizeDatasPair = [0 for _ in range(len(datas))]
        for i in range(len(datas)):
            self.sizeDatas[i] = datas[i].shape[1]
            self.sizeDatasPair[i] = self.__f(datas[i].shape[1]-2, datas[i].shape[1]) + 1    # TODO: check that this is correct
            self.totalElements = self.totalElements + self.sizeDatasPair[i]
    
    def getInitialIndex(self):
        return 0
    
    def getNextIndex(self, i):
        if i<0:
            raise ColossusException("ParallelListPairExtended.getElement - Index out of lower bounds: Minimum is 0, but asked for the next of "+ str(i))
        if i>=self.getFinalIndex():
            raise ColossusException("ParallelListPairExtended.getElement - Index out of upper bounds: Maximum is " + str(self.getFinalIndex()) + ", but asked for the next of " + str(i))
        return i+1;
    
    def getFinalIndex(self):
        return self.totalElements-1
    
    '''
    Here, we must take into account the sizes of each data set to choose the proper element. First, we must undertake a search to
    determine which data set corresponds the element. Then we must perform the same search as did in the ParallelListPair class 
    considering only one data source.
    
    Return [currentDataIndex, ii, jj], where currentDataIndex is the index of the datasource where the element 'i' belongs to,
    and ii, jj are the indexes inside the datasource currentDataIndex that represent the element.
    '''
    def getElement(self, i):
        # First, we check for possible errors
        if i<0:
            raise ColossusException("ParallelListPairExtended.getElement - Index out of lower bounds: Minimum is 0, but asked for "+ str(i))
        if i>self.getFinalIndex():
            raise ColossusException("ParallelListPairExtended.getElement - Index out of upper bounds: Maximum is " + str(self.getFinalIndex()) + ", but asked for " + str(i))
    
        # Now we look for the corresponding data source
        datasetIndex = 0
        accum = 0
        while accum <= i:
            accum = accum + self.sizeDatasPair[datasetIndex]
            datasetIndex = datasetIndex + 1
           
        
        currentDataIndex = datasetIndex-1
        
        # Now we check the concrete pair of elements inside the dataset selected
        newI = i - (accum - self.sizeDatasPair[currentDataIndex])
        N = self.sizeDatas[currentDataIndex]
        ii=0
        jj=1
        order = 0
        while (order < newI):
            if jj == N-1:
                ii=ii+1
                jj=ii+1
            else:
                jj=jj+1
            
            order = order + 1
              
        return [currentDataIndex, ii,jj];
    
    
    '''
    Return the number of pair elements: In a list of N elements, the total combinations of sorted pairs is __f(N-2,N) + 1  
    '''
    def __f(self,i, N):
        return i * (2*N - i - 1) / 2
        
    @abc.abstractmethod
    def processElement(self, x, id=None):
        return 

    @abc.abstractmethod
    def merge(self, out1, out2, id=None):
        return
    
class ParallelListPair(Colossus.core.kernel.parallel_gen.ParallelGen):
    '''
    Abstract class that considers input data as a list of elements, but where the process is taken by the index of pair of elements of the list.
    So, if list is x[0], x[1], x[2], x[4] ... the process element will be [0,1], [0,2], [0,3],[0,4]... [1,2], [1,3], [1,4] ... [2, 3] [2, 4]...
    
    Two methods to be implemented:
    processElement (x), ret X:f(x), it returns f(x), which is of type X . Here, x=[i1,i2], a list of two elements
    merge(x1,x2) ret X:f(x1,x2). where x1 and x2 are of type X, and f(x1,x2) is also of type X
    '''
    __metaclass__ = abc.ABCMeta
    #def __init__(self, data):
    #    self.data=data
    #    if (len(data) < 2):
    #        msg = "Input data must contain at least two elements"
    #        raise Colossus.exception.exceptions.ColossusException(msg)
        
    def getInitialIndex(self):
        return 0
    
    def getFinalIndex(self):
        N = len(self.data)
        return self.__f(N-2)
    
    def __f(self,i):
        N = len(self.data)
        return i * (2*N - i - 1) / 2
        
    def getNextIndex(self, i):
        return i+1;
    
    def getElement(self, i):
        N = len(self.data)
        ii=0
        jj=1
        order = 0
        while (order < i):
            if jj == N-1:
                ii=ii+1
                jj=ii+1
            else:
                jj=jj+1
            
            order = order + 1
              
        return [ii,jj];
    
    @abc.abstractmethod
    def processElement(self, x, id=None):
        return 

    @abc.abstractmethod
    def merge(self, out1, out2, id=None):
        return