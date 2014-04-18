# (C) 2013 iMath Research S.L. - All rights reserved.
""" A test to verify that the same result is achieved when the job is divided into
 several parallel threads. 
 The test, generates a list of random numbers and the result is the sum of all numbers that
 are prime.
 It uses te abstract class ParallelList
Authors:

@author iMath
"""

import math
import random
import time
import unittest
import Colossus.core.kernel.parallel
#from Colossus.core.kernel.parallel import ParallelList

class SumPrimesParallel(Colossus.core.kernel.parallel.ParallelList):
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

class SumPrimes_Test(unittest.TestCase):
    def setUp(self):
        self.n = 4000000
        self.data = [random.randint(0,1000) for _ in range(0,self.n)]
    
    def test_base(self):
        # try with one cpu
        aux = SumPrimesParallel([1,2,3])
        res1 = aux.startProcess()
        self.assertEqual(res1,5)
        
        aux = SumPrimesParallel([1,2,3])
        res2 = aux.startProcess(1)
        self.assertEqual(res2,5)
        
    def test_main(self):
        
        aux = SumPrimesParallel(self.data)
        #print aux.data
        start_time = time.time()
        res1 = aux.startProcess()
        print "The result is " + str(res1)
        print "elapsed time now: ", time.time()-start_time

        start_time = time.time()
        res2 = aux.start()
        print "The result is " + str(res2)
        print "elapsed time before (should be the same as before): ", time.time()-start_time

        start_time = time.time()
        res3 = aux.startProcess(1)
        print "The result is " + str(res3)
        print "elapsed time NO PARALLEL: ", time.time()-start_time
        self.assertEqual(res1,res2)
        self.assertEqual(res2,res3)
        
if __name__ == '__main__':
    unittest.main()