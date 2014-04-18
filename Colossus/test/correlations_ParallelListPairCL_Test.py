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
from Colossus.core.extended.parallel_cl import ParallelListPairCL
import csv

class CorrelationParallel_Test(unittest.TestCase):
    def setUp(self):
        print "Creating data"
        self.n = 40000
        self.m = 20
        self.data = []
        for i in range(0,self.m):
            #print i 
            self.data.append([random.randint(0,1000) for _ in range(0,self.n)])
        
        with open('test.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            for i in range(0,self.n):
                row = []
                for j in range(0,self.m):
                    row.append(self.data[j][i])
                
                spamwriter.writerow(row)
            
        print "done creating data"
        
        '''
        x = [random.randint(0,1000) for _ in range(0,self.n)]
        y = [random.randint(0,1000) for _ in range(0,self.n)]
        z = [random.randint(0,1000) for _ in range(0,self.n)]
        t = [random.randint(0,1000) for _ in range(0,self.n)]
        u = [random.randint(0,1000) for _ in range(0,self.n)]
        self.data = [x,y,z, t, u]
        '''
            
    def test_main(self):
        #path = "/media/ipinyol/DATA/workspace3/iMathCloud_Plugin/Colossus/test/"
        path = "/home/andrea/workspace/iMathCloud_Plugin/Colossus/test/"
        procesElem = "python " + path + "processElementTest.py"
        merge = "python " + path + "mergeTest.py"
        aux = ParallelListPairCL(self.data, procesElem, merge)
        
        #print aux.data
        start_time = time.time()
        res1 = aux.startProcess(1)
        print "The result is " + str(res1)
        print "elapsed time NO-PARALLEL: ", time.time()-start_time
        
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