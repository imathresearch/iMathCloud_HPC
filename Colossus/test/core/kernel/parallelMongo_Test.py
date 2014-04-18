'''
Created on 25/03/2014

@author: andrea
'''
import time

import unittest
from pymongo import MongoClient

from Colossus.core.kernel.parallelMongo import ParallelMongo
from Colossus.exception.exceptions import ColossusException

class Parallel_Mongo(ParallelMongo):
    
    def processElement(self, inp, id=None):
        value = inp['x']
        return value*value
    
    def merge(self,out1, out2, id=None):
        elem = out1 + out2
        document = {"y" : elem}
        self.writeToDB(document, 'test_db', 'test_result', '158.109.125.44', 27017)
        return out1 + out2 


class ParallelMongo_Test(unittest.TestCase):
    """
        To run the test, check the IP of the Mongo Database
    """

    def setUp(self):
        'we connect to mongo localhost'
        self.client = MongoClient()
        
        self.mydb = self.client['test_db']
        self.mycol = self.mydb['test_colection']
        self.mycol.remove()
        self.mycol_result = self.mydb['test_result']
        self.mycol_result.remove()
        
        for i in range (0, 20):
            self.mycol.insert( { 'x' : i } )
        
        
    def tearDown(self):
        pass


    def test_Basic(self):
        pm = Parallel_Mongo('test_db', 'test_colection', '158.109.125.44', 27017)
        
        ###### check method getInitialIndex
        self.assertEqual(pm.getInitialIndex(), 0)
        
        ###### check method getFinalIndex
        self.assertEqual(pm.getFinalIndex(), 19)
              
        ###### check method getElement      
        for i in range (0,20):
            self.assertEqual(pm.getElement(i)['x'], i)
            
        ###### check method getNextIndex
        # input below 0 must raise an exception
        with self.assertRaises(ColossusException):
            pm.getNextIndex(-1)
        
        with self.assertRaises(ColossusException):
            pm.getNextIndex(-100)
        
        #input higher or the same than the maximum number of pair elements must raise an exception
        with self.assertRaises(ColossusException):
            pm.getNextIndex(19)
         
        #input higher or the same than the maximum number of pair elements must raise an exception
        with self.assertRaises(ColossusException):
            pm.getNextIndex(100)
        
        # The general case
        self.assertEqual(pm.getNextIndex(0), 1)
        self.assertEqual(pm.getNextIndex(10), 11)
        self.assertEqual(pm.getNextIndex(18), 19)
    
     
    def test_main(self):
        """
             Test the class ParallelMongo running locally and remotely
        """
        
        pm = Parallel_Mongo('test_db', 'test_colection', '158.109.125.44', 27017)
        
        start_time = time.time()
        result1 = pm.startProcess(4)
        print "The result is " + str(result1)
        print "elapsed time sequencial : ", time.time()-start_time
        
        start_time = time.time()
        result2 = pm.startProcess()
        print "The result is " + str(result2)
        print "elapsed time parallel : ", time.time()-start_time
       
        self.assertEqual(result1, result2)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()