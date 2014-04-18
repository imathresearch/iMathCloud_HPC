# (C) 2013 iMath Research S.L. - All rights reserved.
""" A test to verify that the same result is achieved when the job is divided into
 several parallel threads. 
 The test, generates a list of random numbers from 0 to 20 and the result is a list of
 each number with the number of times that appears in the list. So, it is the classical example 
 used in Map/Reduce paradigm for word counting
 
 It uses the Class ParallelMapReduce 

Authors:

@author iMath
"""

import math
import random
import time
import unittest
from Colossus.core.kernel.parallel import ParallelMapReduce

class WordsCountParallel(ParallelMapReduce):
    def map(self,x):
        return self.generatePair(x, 1)

    def reduce(self,v1,v2):
        return v1+v2
    
    def getCommandParameters(self):
        pass
    
    def prepareClientData(self):
        pass
    
class SumPrimes_Test(unittest.TestCase):
    def setUp(self):
        #self.n = 50000000
        self.n = 500
        self.data = [random.randint(0,20) for _ in range(0,self.n)]
    
    def test_base(self):
        # try with one cpu
        aux = WordsCountParallel([1,1,3,4,3,3])
        res1 = aux.start(1)
        self.assertEqual(res1[1],2)
        self.assertEqual(res1[3],3)
        self.assertEqual(res1[4],1)
                
        # try with optimum cpus
        res1 = aux.start()
        self.assertEqual(res1[1],2)
        self.assertEqual(res1[3],3)
        self.assertEqual(res1[4],1)
        
    def test_main(self):
        
        aux = WordsCountParallel(self.data)
        """#print aux.data
        start_time = time.time()
        res1 = aux.start(1)
        print "The result is " + str(res1)
        print "elapsed time NO-PARALLEL: ", time.time()-start_time

        start_time = time.time()
        res2 = aux.start()
        print "The result is " + str(res2)
        print "elapsed time PARALLEL OPTIMUM: ", time.time()-start_time
        """
        start_time = time.time()
        res3 = aux.startProcess()
        print "The result is " + str(res3)
        print "elapsed time PARALLEL OVER PARALLEL (Now): ", time.time()-start_time
        
        
if __name__ == '__main__':
    unittest.main()