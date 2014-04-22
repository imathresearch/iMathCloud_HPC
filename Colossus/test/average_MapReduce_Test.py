# (C) 2013 iMath Research S.L. - All rights reserved.
""" A test to verify that the same result is achieved when the job is divided into
 several parallel threads. 
 The test, implements the following select:
 
 Select age, AVG(contacts)
 from users
 group by age

So, we achieve the average contacts per age range, using our variation of map/reduce over Colossus

We assume data is a list of tuple [id, age, #contacts]

Authors:

@author iMath
"""

import math
import random
import time
import unittest
from Colossus.core.kernel.parallel import ParallelMapReduce

class AverageAge(ParallelMapReduce):
    def map(self,x):
        ' Here, x represents a row [id, age, #contacts]. '
        ' So, our key is the age, stored in x[1], and the value will be the accumulated average. Since it is an accumulated average '
        ' we need to store as well the number of instances used to calculate the average, if not, merge will not work'
        return self.generatePair(x[1], [float(x[2]),1])

    def reduce(self,v1,v2):
        'Here, v1 and v2 are the values (see map function), and the result is a new value a new value with the new accumulated average'
        contacts1 = v1[0]
        contacts2 = v2[0]
        num1 = v1[1]
        num2 = v2[1]
        newNum = num1 + num2
        newAvg = (contacts1*num1 + contacts2*num2) / newNum
        return [newAvg, newNum]
    
    def getCommandParameters(self):
        pass
    
    def prepareClientData(self):
        pass
    
    
class AverageAge_Test(unittest.TestCase):
    def setUp(self):
        self.n = 10000000
        'we generate random tuples of data, with single id. Age range between 10 and 60, and contacts between 0 and 20'
        self.data = [[x,y,z] for x in range(0,self.n) for y in [random.randint(10,60)] for z in [random.randint(0,20)]]
    
    def test_main(self):
        
        aux = AverageAge(self.data)
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
        res2 = aux.startProcess()
        print "The result is " + str(res2)
        print "elapsed time PARALLEL OPTIMUM NEW: ", time.time()-start_time
        
        '''
        start_time = time.time()
        res3 = aux.start(10)
        print "The result is " + str(res3)
        print "elapsed time PARALLEL OVER PARALLEL (10): ", time.time()-start_time
        '''
        
if __name__ == '__main__':
    unittest.main()