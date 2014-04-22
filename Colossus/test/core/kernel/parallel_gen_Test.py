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
        At the moment of performing the test, we simulate this file and its content:
           Host andrea-H61H2-I3
           User andrea
           Hostname 158.109.125.44

           Host pesto
           User ammartinez
           Hostname 158.109.125.35
        
        Change the path of the simulated ssh_config file to be correct in your machine

    """
    def test_getDataHost(self):
        pg = ButlerCorrelationParallel(self.data)
        
        name_file = "/home/andrea/ssh_config_file.txt";
        file = open(name_file, "w");

        lines_of_text = ["Host andrea-H61H2-I3\n", "User andrea\n", "Hostname 158.109.125.44\n", "Host pesto\n", "User ammartinez\n", "Hostname 158.109.125.35\n"]
        file.writelines(lines_of_text)
        file.close()

        
        host1 = 'andrea-H61H2-I3'
        host2 = 'pesto'
        
        data_host1 = pg.getDataHosts(host1, name_file)
        data_host2 = pg.getDataHosts(host2, name_file)
        
        self.assertEqual(len(data_host1), 2)
        self.assertEqual(len(data_host2), 2)
        
        self.assertEqual(data_host1['hostname'], '158.109.125.44')
        self.assertEqual(data_host2['hostname'], '158.109.125.35')
        self.assertEqual(data_host1['user'], 'andrea')
        self.assertEqual(data_host2['user'], 'ammartinez')
    
    """
        Put the number of cpus of your machine in the variable num_cpus
    """  
    def test_connecToHost(self):
        pg = ButlerCorrelationParallel(self.data)
        
        host = '127.0.0.1'
        num_cpus = 4;
        
        client_host = pg.connecToHost(host) 
        #client_host2 = pg.connecToHost(host2)
        
        #We check that in fact we have connected to these hosts
        stdin, stdout, stderr = client_host.exec_command('grep processor /proc/cpuinfo')
        #stdin2, stdout2, stderr2 = client_host2.exec_command('uname -n')
        
        self.assertEqual(len(stdout.readlines()), num_cpus)
        #self.assertEqual(host2, stdout2.read().rstrip('\n'))
    
    """
        Put the number of cpus of your machine in the variable num_cpus
    """
    def test_getCPUs(self):
        pg = ButlerCorrelationParallel(self.data)
        
        #My machine has 4 cores
        host1 = '127.0.0.1'
        num_cpus = 4;
        
        ncpus = pg.getCPUs(host1)
        
        self.assertEqual(ncpus, num_cpus)
    
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
        We suppose that the server is running on localhost 127.0.0.1
    """
    def test_setQueueInfo(self):
        pg = ButlerCorrelationParallel(self.data)
      
        #andrea-H61H2-I3
        hosts = ['yourmachine']
        
        #The master server of Colossus is started, and a shared queue with 'yourmachine' is stablished
        master_server = pg.getMasterServer(hosts)
        
        hostInfo = []      
        hostInfo.append(['yourmachine',4])
        parts = pg.getPart(4)
        init = pg.getInitialIndex()
        end = pg.getFinalIndex() 
        pairs = pg.getPairs(init, end, parts)
        #The info for the clients is set in the queues
        pg.setInfoClients(master_server, hostInfo, pairs, parts)
        
        #The client server is started and connected to the master server of Colossus
        client_manager = pg.getClientManager()          
        inputQ = client_manager.getInputQueue('yourmachine')  # Get the input queue corresponding to this Host
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