# (C) 2013 iMath Research S.L. - All rights reserved.
""" A test to verify that the same result is achieved when the job is divided into
 several parallel threads. 
 The test generates a random matrix of N columns and calculate the pearsons correlation of 
 each column with each column, using ParallelListPair
Authors:

@author iMath
"""

import math
import random
import time
import unittest
from Colossus.core.kernel.parallel import ParallelListPair
from scipy.stats.stats import pearsonr

class CorrelationParallel(ParallelListPair):
    def processElement(self, inp, id=None):
        
        i0 = inp[0]
        i1 = inp[1]
        start_time = time.time()
        r = pearsonr(self.data[i0], self.data[i1])
        #print "elapsed time: ", time.time()-start_time
        #print i0,i1, r
        return [[i0, i1, r]]
    
    def merge(self,out1, out2, id=None):
        return out1 + out2
    
    def getCommandParameters(self):
        pass
    
    def prepareClientData(self):
        pass
    
class CorrelationParallel_Test(unittest.TestCase):
    def setUp(self):
        print "Creating data"
        self.n = 4
        self.data = []
        for i in range(0,5):
            #print i 
            self.data.append([random.randint(0,1000) for _ in range(0,self.n)])
        
        print "done creating data"
        
        print self.data
        print len(self.data)
        '''
        x = [random.randint(0,1000) for _ in range(0,self.n)]
        y = [random.randint(0,1000) for _ in range(0,self.n)]
        z = [random.randint(0,1000) for _ in range(0,self.n)]
        t = [random.randint(0,1000) for _ in range(0,self.n)]
        u = [random.randint(0,1000) for _ in range(0,self.n)]
        self.data = [x,y,z, t, u]
        '''
            
    def test_main(self):
        
        aux = CorrelationParallel(self.data)
        
        #print aux.data
        start_time = time.time()
        """res1 = aux.startProcess(1)
        print "The result is " + str(res1)
        print "elapsed time NO-PARALLEL: ", time.time()-start_time
        """
        start_time = time.time()
        res2 = aux.startProcess()
        print "The result is " + str(res2)
        print "elapsed time PARALLEL OPTIMUM: ", time.time()-start_time
        
        '''
        start_time = time.time()
        res3 = aux.start(10)
        print "The result is " + str(res3)
        print "elapsed time PARALLEL OVER PARALLEL (10): ", time.time()-start_time
        '''
        
if __name__ == '__main__':
    unittest.main()