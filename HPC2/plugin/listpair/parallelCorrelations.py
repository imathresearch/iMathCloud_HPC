'''
Created on Dec 18, 2013

@author: iMath
'''
from Colossus.core.kernel.parallel import ParallelListPair
from scipy.stats.stats import pearsonr


class CorrelationParallel(ParallelListPair):
    def processElement(self, inp, id=None):
        
        i0 = inp[0]
        i1 = inp[1]
        r = pearsonr(self.data[i0], self.data[i1])
        return [[i0, i1, r[0]]]
    
    def merge(self,out1, out2, id=None):
        return out1 + out2 
   