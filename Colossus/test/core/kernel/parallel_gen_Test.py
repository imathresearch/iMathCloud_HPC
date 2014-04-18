'''
Created on 21/03/2014

@author: andrea
'''
import unittest
import numpy
import random
from Colossus.core.kernel.parallel_gen import ParallelGen
from HPC2.plugin.listpair.butlerCorrelations import ButlerCorrelationParallel



class Parallel_gen_Test(unittest.TestCase):


    def setUp(self):
        
        n = 5
        data = []
        for i in range(0,10):
            data.append([random.randint(0,1000) for _ in range(0,n)])

        datas = []
        aux = numpy.array(data) + 1
        datas = datas + [aux]
        
        self.data = datas
        
       

    def tearDown(self):
        pass


    """
        Tests test_getHosts and test_getSortedHosts depend on the file where the name of the available host is stored
        At the moment of performing the test, the content of my file is
           andrea-H61H2-I3
           pesto
    """
    def test_getHosts(self):
        pg = ButlerCorrelationParallel(self.data)
           
        list_hosts = pg.getHosts()

        self.assertEqual(len(list_hosts), 2)
        self.assertIn('andrea-H61H2-I3', list_hosts)
        self.assertIn('pesto', list_hosts)
        
    def test_getSortedHosts(self):
        pg = ButlerCorrelationParallel(self.data)
        
        list_hosts = pg.getHosts();
        
        sorted_hosts = pg.getSortedHosts(list_hosts)
        
        for i in range (1, len(sorted_hosts)-1):
            self.assertGreaterEqual(sorted_hosts[i][2], sorted_hosts[i+1][2])
    
    """
        The tests test_getDataHost, test_connecToHost and test_getCPUs depend on the file config located at .ssh/ where the information about the 
        available machines have to be available
        At the moment of performing the test, the content of this file is my computer is
           Host andrea-H61H2-I3
           User andrea
           Hostname 158.109.125.44

           Host pesto
           User ammartinez
           Hostname 158.109.125.35

    """
    def test_getDataHost(self):
        pg = ButlerCorrelationParallel(self.data)
        
        host1 = 'andrea-H61H2-I3'
        host2 = 'pesto'
        
        data_host1 = pg.getDataHosts(host1)
        data_host2 = pg.getDataHosts(host2)
        
        self.assertEqual(len(data_host1), 2)
        self.assertEqual(len(data_host2), 2)
        
        self.assertEqual(data_host1['hostname'], '158.109.125.44')
        self.assertEqual(data_host2['hostname'], '158.109.125.35')
        self.assertEqual(data_host1['user'], 'andrea')
        self.assertEqual(data_host2['user'], 'ammartinez')
        
    def test_connecToHost(self):
        pg = ButlerCorrelationParallel(self.data)
        
        host1 = 'andrea-H61H2-I3'
        host2 = 'pesto'
        
        client_host1 = pg.connecToHost(host1) 
        client_host2 = pg.connecToHost(host2)
        
        #We check that in fact we have connected to these hosts
        stdin1, stdout1, stderr1 = client_host1.exec_command('uname -n')
        stdin2, stdout2, stderr2 = client_host2.exec_command('uname -n')
        
        self.assertEqual(host1, stdout1.read().rstrip('\n'))
        self.assertEqual(host2, stdout2.read().rstrip('\n'))
     
    def test_getCPUs(self):
        pg = ButlerCorrelationParallel(self.data)
        
        #My machine has 4 cores
        host1 = 'andrea-H61H2-I3'
        ncpus = pg.getCPUs(host1)
        
        self.assertEqual(ncpus, 4)
    
    """
        The goal of this test is to check that the remote queus between a master server of colossus
        and a client are connected and the data transfer is OK
        To do it, we have to lunch the master server (default is lunch on my machine) and connect a client
        to this server (it is also lunched in my machine).
        So, we check that the data put in the queues by the master server are the same data received by
        the client, and viceversa the client puts a result in the master queues, and it is expected that
        the same value is received by the master.
        With this test, we are testing the following functions:
        - __runMasterServer
        - __setQueueInfo (Colossus server side)
        - __startClientManager
    """
    def test_setQueueInfo(self):
        pg = ButlerCorrelationParallel(self.data)
      
        hosts = ['andrea-H61H2-I3']
        
        #The master server of Colossus is started, and a shared queue with 'andrea-H61H2-I3' is stablished
        master_server = pg.getMasterServer(hosts)
        
        hostInfo = []      
        hostInfo.append(['andrea-H61H2-I3',4])
        #My machine only have 4 cpus
        parts = pg.getPart(4)
        init = pg.getInitialIndex()
        end = pg.getFinalIndex() 
        pairs = pg.getPairs(init, end, parts)
        #The info for the clients is set in the queues
        pg.setInfoClients(master_server, hostInfo, pairs, parts)
        
        #The client server is started and connected to the master server of Colossus
        client_manager = pg.getClientManager()          
        inputQ = client_manager.getInputQueue('andrea-H61H2-I3')  # Get the input queue corresponding to this Host
        outputQ = client_manager.getOutputQueue()  # Get the output queue        
        parts_client = inputQ.get()                # Get the increment between batches
        init_client = inputQ.get()                 # Get the initial point
        end_client = inputQ.get()                  # Get the final point
    
        #As we only have one host client, the init and end parts of the data for the client, are the same
        #as the initial calculated.
        self.assertEqual(parts_client, parts)
        self.assertEqual(init_client, init)
        self.assertEqual(end_client, end)
        
        
        outputQ.put(parts*init*end)   
        q = master_server.getOutputQueue()
        
        self.assertEqual(q.get(),parts*init*end)
        
    
            
        
        
           

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()