'''
Created on Dec 18, 2013

@author: iMath
'''
from Colossus.core.kernel.parallelFile import ParallelFile
#from Colossus.core.kernel.parallelListPair import ParallelListPairExtended
from scipy.stats.stats import pearsonr
from HPC2.common.constants import CONS
import pickle

CONS = CONS()

'''
The Colossus class that implements ParallelListPairExtended, to perform ListPair processing considering multile data source
We consider self.data is a list of numpy arrays. Numpy array 'i' is of shape N_i x M_i. 
'''
#class ButlerCorrelationParallel(ParallelListPairExtended):
class ButlerCorrelationParallel(ParallelFile):
    
    def processElement(self, inp, id=None):
        key = inp[0]
        i0 = inp[1]
        i1 = inp[2]
        r = pearsonr(self.data[key][:,i0], self.data[key][:,i1])
        return self.__map(key,[[i0, i1, r[0]]])
    
    def merge(self,out1,out2, id=None):
        for key in out2.iterkeys():
            value = out2[key]
            if (key in out1):
                value2 = out1[key]
                out1[key] = self.__reduce(value, value2)
            else:
                out1[key] = value
        
        return out1
    
    def __map(self, key, elem):
        return dict({key:elem})
    
    def __reduce(self, v1, v2):
        return v1 + v2
     
    def getCommandParameters(self):
        return [CONS.FILECLIENTDATA]
        
    def prepareClientData(self):
        #We save the data for the clients
        #print CONS.FILECLIENTDATA
        pickle.dump(self.data, open(CONS.FILECLIENTDATA, "wb" ) )
