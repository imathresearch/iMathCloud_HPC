'''
Created on 30/12/2013

@author: iMath
'''

import random
import time
import unittest
from Colossus.core.kernel.parallelListPair import ParallelListPairExtended
from scipy.stats.stats import pearsonr
from Colossus.exception.exceptions import ColossusException
import numpy as np

class CorrelationParallel(ParallelListPairExtended):
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
    
class ParallelListPairExtended_Test(unittest.TestCase):
    def setUp(self):
        print "Creating data"
        self.n = 40000
        self.data1 = []
        for i in range(0,20):
            aux = [random.randint(0,1000) for _ in range(0,self.n)]
            self.data1.append([random.randint(0,1000) for _ in range(0,self.n)])
        
        self.n = 400
        self.data2 = []
        for i in range(0,50):
            self.data2.append([random.randint(0,1000) for _ in range(0,self.n)])
            
        self.n = 200
        self.data3 = []
        for i in range(0,5):
            self.data3.append([random.randint(0,1000) for _ in range(0,self.n)])
        
        
        print "done creating data"
        
    '''
    test the case bases of public methods related to indexes
    '''
    def test_basic(self):
        data = [np.array(self.data1).transpose(), np.array(self.data2).transpose(), np.array(self.data3).transpose()]
        testClass = CorrelationParallel(data)
        
        ###### check that getFinalIndex returns 1424, as we have 3 data sources of 20, 50 and 5 elements.
        self.assertEqual(testClass.getFinalIndex(), 1424)
        ####################
        
        ###### check getInitialIndex is 0
        self.assertEqual(testClass.getInitialIndex(), 0)
        ####################
        
        ###### check method getNextIndex
        # input below 0 must raise an exception
        with self.assertRaises(ColossusException):
            testClass.getNextIndex(-1)
        
        with self.assertRaises(ColossusException):
            testClass.getNextIndex(-500)
        
        #input higher or the same than the maximum number of pair elements must raise an exception
        with self.assertRaises(ColossusException):
            testClass.getNextIndex(1424)
         
        #input higher or the same than the maximum number of pair elements must raise an exception
        with self.assertRaises(ColossusException):
            testClass.getNextIndex(5000)
        
        # The general case
        self.assertEqual(testClass.getNextIndex(0), 1)
        self.assertEqual(testClass.getNextIndex(1423), 1424)
        self.assertEqual(testClass.getNextIndex(48), 49)
        
        ####################
    
    '''
    Test the method getElement  
    '''
    def test_elem(self):
        #data = [self.data1, self.data2, self.data3]
        data = [np.array(self.data1).transpose(), np.array(self.data2).transpose(), np.array(self.data3).transpose()]
        testClass = CorrelationParallel(data)
        
        # when parameter is below 0, an exception is raised
        #input higher or the same than the maximum number of pair elements must raise an exception
        with self.assertRaises(ColossusException):
            testClass.getNextIndex(-1)
        
        with self.assertRaises(ColossusException):
            testClass.getNextIndex(-100)
        
        
        # when parameter is higher than then maximum, an exception is raised
        with self.assertRaises(ColossusException):
            testClass.getNextIndex(1425)
        
        # when parameter is higher than then maximum, an exception is raised
        with self.assertRaises(ColossusException):
            testClass.getNextIndex(15000)
        
        # Now we try the general cases on the extremes:
        self.assertEqual(testClass.getElement(0), [0,0,1])
        self.assertEqual(testClass.getElement(1424), [2,3,4])
        
        self.assertEqual(testClass.getElement(189), [0,18,19])
        self.assertEqual(testClass.getElement(190), [1,0,1])
        
        self.assertEqual(testClass.getElement(1414), [1,48,49])
        self.assertEqual(testClass.getElement(1415), [2,0,1])

        # And some general cases
        self.assertEqual(testClass.getElement(1), [0,0,2])
        self.assertEqual(testClass.getElement(2), [0,0,3])
        self.assertEqual(testClass.getElement(3), [0,0,4])
        
        # And some general cases
        self.assertEqual(testClass.getElement(191), [1,0,2])
        self.assertEqual(testClass.getElement(192), [1,0,3])
        self.assertEqual(testClass.getElement(193), [1,0,4])
        
        # And some general cases
        self.assertEqual(testClass.getElement(1416), [2,0,2])
        self.assertEqual(testClass.getElement(1417), [2,0,3])
        self.assertEqual(testClass.getElement(1418), [2,0,4])
        self.assertEqual(testClass.getElement(1419), [2,1,2])
        
if __name__ == '__main__':
    unittest.main()