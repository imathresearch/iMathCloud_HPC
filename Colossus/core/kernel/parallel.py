# (C) 2013 iMath Research S.L. - All rights reserved.
""" The abstract class that implements parallel tasks in Colossus  
job in the current host and 

Authors:

@author iMath
"""

import abc
import Colossus.exception.exceptions
import Colossus.core.kernel.parallel_gen
#from Colossus.exception.exceptions import ColossusException
#from Colossus.core.kernel.parallel_gen import ParallelGen
import numpy as np

   
class ParallelList(Colossus.core.kernel.parallel_gen.ParallelGen):
    '''
    Abstract class that considers input data as a list of elements. So, the process is taken element by element.
    Two methods to be implemented:
    processElement (x), ret X:f(x), it returns f(x), which is of type X 
    merge(x1,x2) ret X:f(x1,x2). where x1 and x2 are of type X, and f(x1,x2) is also of type X
    '''
    __metaclass__ = abc.ABCMeta
    def __init__(self, data):
        self.data=data

    def getInitialIndex(self):
        return 0
    
    def getFinalIndex(self):
        return len(self.data)-1;
    
    def getNextIndex(self, i):
        return i+1;
    
    def getElement(self, i):
        return self.data[i];
    
    @abc.abstractmethod
    def processElement(self, x):
        return 

    @abc.abstractmethod
    def merge(self, out1, out2):
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
    
    
class ParallelMatrix(Colossus.core.kernel.parallel_gen.ParallelGen):
    '''
    classdocs
    Parallel processing for numpy matrix
    '''
    __metaclass__ = abc.ABCMeta
    N = -1
    M = -1
    def __init__(self, data):
        self.data=data
        size = np.shape(self.data)
        if (len(size) != 2):
            msg = "Input data must be a numpy array of two dimensions"
            raise Colossus.exception.exceptions.ColossusException(msg)
        self.N = size[0]
        self.M = size[1]

    def getInitialIndex(self):
        return 0
    
    def getFinalIndex(self):
        return self.N * self.M -1;
    
    def getNextIndex(self, i):
        return i+1;
    
    def getElement(self, i):
        jj = i % self.M
        ii = (i - jj) / self.M
        return self.data[ii][jj]
    
    @abc.abstractmethod
    def processElement(self, x):
        return 

    @abc.abstractmethod
    def merge(self, out1, out2):
        return

class ParallelMapReduce(ParallelList):
    '''
    Abstract class that implements a reduced version of Map/Reduce API
    
    Two methods to be implemented:
    
    map(x) -> The map function, which receives as entry, an element of the list. The output must be a par <key:, value>, generated with the function
                generatePair. The type of 'value' is X, and the type of key is Y
                
    reduce(x,y) -> Given x, y of type X (value), it returns another element of type X. It should implement reduce function as in the standard
                map/reduce API, where imlements how the elements that have the same key are aggregated
    '''
    __metaclass__ = abc.ABCMeta
    def __init__(self, data):
        self.data=data

    @abc.abstractmethod
    def map(self, x):
        return 
    
    @abc.abstractmethod
    def reduce(self,x,y):
        return
    
    def generatePair(self,k,v):
        return dict({k:v})
    
    def processElement(self, x, id=None):
        return self.map(x)

    def merge(self,out1,out2, id=None):
        for key in out2.iterkeys():
            value = out2[key]
            if (key in out1):
                value2 = out1[key]
                out1[key] = self.reduce(value, value2)
            else:
                out1[key] = value
        
        return out1
    