# (C) 2013 iMath Research S.L. - All rights reserved.
""" A test to verify that the same result is achieved when the job is divided into
 several parallel threads. 
 The test, generates a matrix of random numbers and the result is the sum of all numbers that
 are prime.
 It uses the abstract Class ParallelMatrix

Authors:

@author iMath
"""

import math
import random
import time
import unittest
from Colossus.core.kernel.parallel import ParallelMatrix
import numpy as np

class Test(ParallelMatrix):
    def processElement(self,x, id=None):
        if (self.isprime(x)):
            return x
        return 0
    
    def merge(self,out1,out2, id=None):
        return out1 + out2
    
    def isprime(self,n):
        """Returns True if n is prime and False otherwise"""
        if not isinstance(n, int):
            raise TypeError("argument passed to is_prime is not of 'int' type")
        if n < 2:
            return False
        if n == 2:
            return True
        maxim = int(math.ceil(math.sqrt(n)))
        i = 2
        while i <= maxim:
            if n % i == 0:
                return False
            i += 1
        return True
    
    def getCommandParameters(self):
        pass
    
    def prepareClientData(self):
        pass

class SumPrimes_Test(unittest.TestCase):
    def setUp(self):
        self.n = 100000
        self.data = np.array([[random.randint(0,1000) for _ in range(0,self.n)], [random.randint(0,1000) for _ in range(0,self.n)], [random.randint(0,1000) for _ in range(0,self.n)], [random.randint(0,1000) for _ in range(0,self.n)]])
    
    def test_main(self):
        
        aux = Test(self.data)
        #print aux.data
        start_time = time.time()
        res1 = aux.start(1)
        print "The result is " + str(res1)
        print "elapsed time NO-PARALLEL: ", time.time()-start_time

        start_time = time.time()
        res2 = aux.start()
        print "The result is " + str(res2)
        print "elapsed time PARALLEL OPTIMUM: ", time.time()-start_time

        start_time = time.time()
        res3 = aux.start()
        print "The result is " + str(res3)
        print "elapsed time PARALLEL OVER PARALLEL (10): ", time.time()-start_time
        
        #start_time = time.time()
        #res4 = aux.start(0, self.n-1,20)
        #print "The result is " + str(res4)
        #print "elapsed time PARALLEL OVER PARALLEL(20): ", time.time()-start_time
        
        self.assertEqual(res1, res2)
        self.assertEqual(res2, res3)
        #self.assertEqual(res3, res4)
        
if __name__ == '__main__':
    unittest.main()