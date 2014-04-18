# (C) 2013 iMath Research S.L. - All rights reserved.
""" The abstract class that implements parallel tasks in Colossus  
job in the current host and 

Authors:

@author iMath
"""

import abc

import paramiko
import socket
import os
import pickle

#import math
#from Colossus.exception.exceptions import ColossusException
import time
import multiprocessing
import subprocess
from multiprocessing.managers import SyncManager
from Colossus.core.constants import CONS, deprecated


#from multiprocessing import Process
#from multiprocessing import Queue
#from multiprocessing import cpu_count

CONS = CONS()

class ParallelGen(object):
    '''
    classdocs
    
    The abstract class that implements the generic massive parallel exploration among data 
    '''
    
    processElementExternal_subs = dict()
    mergeExternal_subs = dict()
    processElementExternal = None
    mergeExternal=None
    idJob = None                        # The identifier for percentage completeness. Typically it would be the idJob created in iMathCloud 
    ' Used to store threads results'
    resultQueue = multiprocessing.Queue()       
    
    remoteResultQueue = multiprocessing.Queue()
    remoteInputQueues = dict()
    
    __metaclass__ = abc.ABCMeta
    def __init__(self, data, processElementExternal=None, mergeExternal=None, idJob = None):
        self.data=data
        self.processElementExternal = processElementExternal
        self.mergeExternal = mergeExternal
        self.idJob = idJob
    
    @abc.abstractmethod
    def getInitialIndex(self):
        return 0
    
    @abc.abstractmethod
    def getFinalIndex(self):
        return len(self.data)-1;
    
    @abc.abstractmethod
    def getNextIndex(self, i):
        return i+1;
    
    @abc.abstractmethod
    def getElement(self, i):
        return self.data[i];
    
    @abc.abstractmethod
    def processElement(self, x, id=None):
        return
    
    @abc.abstractmethod
    def getCommandParameters(self):
        pass
    
    @abc.abstractmethod
    def prepareClientData(self):
        pass
    
    def __startExternalProcesses(self, numThread):
        if (self.processElementExternal!=None):
            call = self.processElementExternal
            t = subprocess.Popen(call, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            self.processElementExternal_subs[numThread] = t
            self.mergeExternal_subs[numThread] = t
            
        #if (self.mergeExternal!=None):
        #    call = self.processElementExternal
        #    t = subprocess.Popen(call, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)            
        #    self.mergeExternal_subs[numThread] = t

    def __endExternalProcesses(self, numThread):
        if (self.processElementExternal!=None):
            self.processElementExternal_subs[numThread].stdin.write(CONS.ENDPROCESS)
            self.processElementExternal_subs[numThread].stdin.flush()
            self.processElementExternal_subs[numThread].stdin.close()
            
        #if (self.mergeExternal!=None):
        #    self.mergeExternal_subs[numThread].stdin.write(CONS.ENDPROCESS)
        #    self.mergeExternal_subs[numThread].stdin.close()
                   
    def __startMainMerge(self, numThread):
        ' TODO: Check if numThread is already present in the dict, and raise an Exception in this case '
        self.__startExternalProcesses(numThread)
        #if (self.mergeExternal!=None):
        #    call = self.processElementExternal
        #    t = subprocess.Popen(call, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)            
        #    self.mergeExternal_subs[numThread] = t
    
    def __endMainMerge(self, numThread):
        self.__endExternalProcesses(numThread)
        #if (self.mergeExternal!=None):
        #    self.mergeExternal_subs[numThread].stdin.write(CONS.ENDPROCESS)
        #    self.mergeExternal_subs[numThread].stdin.close()
        
    def __partial(self, numThread, init, end, inThread=True):
        
       
        i = init
        condition = True
        self.__startExternalProcesses(numThread)
        
        fd = self.__openTempFile(numThread)     # Create/Open the file for writing the percentages
        self.__writeTempFile(fd, 0)             # Initially, we are at 0% 
        totalElems = end-init + 1
        
        while (condition):
            x = self.getElement(i)
            #print "processing element " +  str(x) + "index " + str(i)
            xAux = self.processElement(x, id = numThread)
            #print "processing element " +  str(x) + "index " + str(i) + ". Resultado " + str(xAux)
            if (i == init):
                acum = xAux
            else:
                acum = self.merge(acum, xAux, id = numThread)
            
            actualElem = i-init + 1
            self.__writeTempFile(fd, float(actualElem) / float(totalElems) * float(100))
            condition = (i!=end)
            if condition:
                j = self.getNextIndex(i)
                i = j
        
        self.__closeTempFile(fd)     # Close the temp file for percentages
        self.__endExternalProcesses(numThread)
        if inThread:
            # Put the result into the queue. Notice that this child process will not end until the
            # parent reads from the queue, which is ok now.
            self.resultQueue.put(acum)
            return 
        else:
            return acum
    
    
    def __openTempFile(self,numThread):
        '''
        Returns the file descriptor of the open file for percentages. 
        Only will be opened when idJob != None
        The temporal file name will be: idJob + "_" + numThread + ".pct
        '''
        fd = None
        if self.idJob !=None:
            fileName = self.__getTempFileName(self.idJob, numThread)
            try:
                fd = open(CONS.PATH_TEMP_FILES + fileName, "w")
                fd.seek(0)
                fd.write("      ")
            except:
                pass
        
        return fd 
    
    def __closeTempFile(self, fd):
        if fd != None:
            try:
                fd.close()
            except:
                pass
    
    def __writeTempFile(self,fd, num):
        if fd !=None:
            try:
                fd.seek(0)
                strNum = '%.2f' % num
                fd.write(strNum)
            except:
                pass
            
    def __getTempFileName(self, idJob, numThread):     
        name = socket.gethostname() + "_" + str(idJob) + "_" + str(numThread)
        return name
    
    
    def __ppJob(self):
        init = self.getInitialIndex()
        end = self.getFinalIndex()    
        self.parts = (end-init+1) / self.ncpus 
        if self.parts <=0:
            self.parts = 1
            
        index = init
        elem = 0
        
        numThreads = 0
        threads = []
        while(index <= end):
            #print "index: ",index, " end: ", end
            init1 = index
            init2 = index+self.parts
            
            if init2 > end:
                init2=end
            #print "[init1, init2] " + str(init1) + " " + str(init2)
            ' We start the subprocesses' 
            t = multiprocessing.Process(target=self.__partial, args=(numThreads, init1, init2, )) 
            t.deamon = True
            threads.append(t)
            t.start()
            numThreads = numThreads + 1
            'jobsOut.append(job_server.submit(self.partial, (init1, init2, ), (),("abc","math",)))'
            #print "##### elapsed time submitting 1 job: ", time.time()-start_time    
            index = init2+1
        
        # We wait for all the subprocesses to end
        # TODO: We should process the partial solutions on the fly, as soon as they arrive
        #for thread in threads:
        #    print "just before joining"
        #    thread.join()
            
        # Finally, we retrieve the results and merge them. 
        if (numThreads > 0):
            ret = self.resultQueue.get()
        i = 1
        
        self.__startMainMerge(-1)
        while(i < numThreads):
            retAux = self.resultQueue.get()
            ret = self.merge(ret, retAux, -1)
            i = i+1
        
        self.__endExternalProcesses(-1)
        return ret
    
    @abc.abstractmethod
    def merge(self, out1, out2, id=None):
        return
    
    @deprecated("ParallelGen", "startProcess")
    def start(self, ncpus = 0):
        # TODO: Multiserver support. Now it only considers one server.
        #ppservers = ()
        #job_server = pp.Server(1, ppservers=ppservers)
        if ncpus <= 0:
            self.ncpus = multiprocessing.cpu_count() # Get the available CPUs
        else:
            self.ncpus = ncpus
        
        #jobsOut = []
        #jobsOut.append(job_server.submit(self.ppJob, (), (), ("abc","math","multiprocessing", "time",), globals=globals()))
        #jobsOut.append(job_server.submit(test, (2000,), (), ("abc","math","multiprocessing", "time",)))
        #jobsOut.append(job_server.submit(test, (2000,), (), ()))
        #jobsOut.append(job_server.submit(self.ppJob, (), (),("abc","math","multiprocessing", "time","Colossus.exception.exceptions","Colossus.core.kernel.parallel_gen", "Colossus.core.kernel.parallel",)))
        #jobsOut.append(job_server.submit(self.partial, (0, 100, ), (),("abc","math",)))
        #print "waiting..."
        ' Now we only have one ppJob'
        #for job in jobsOut:
        #    ret = job()
        #return ret
        return self.__ppJob()
    
    
    ''''
    Server Side
    '''
    
    
    def __getHosts(self):
        """
        This function returns a list that contains the name of the available machines
        This function requires a file referenced in CONS.HOSTFILE, that contains the required names
        """
        
        """
            CLOUD EXECUTION
        """
        list_hostName = [];
        hn=(l.rstrip('\n') for l in file(CONS.HOSTFILE,"Ur"));
        for name in hn:
            list_hostName.append(name);

        return list_hostName;

    
    
    def __getCPUs(self, host):
        """
        This function returns the number of CPUs available in an specific host
        The parameter host corresponds to the name of the machine
        """
        
        if (host== CONS.LOCALHOST):    # The local host
            return multiprocessing.cpu_count()
        else:
            sshclient = self.__connectToHost(host);
            stdin, stdout, stderr = sshclient.exec_command('grep processor /proc/cpuinfo')
        
            return len(stdout.readlines())
         
        return 1
    
    
    def __getDataHost(self, host):
        """
        This function returns a dictionary for the given host
        The structure of the dictionary is the following
        {'hostname': IP, 'user': usernameofthemachine}
        """
        # ssh config file
        config = paramiko.SSHConfig()
        config.parse(open(CONS.SSHCONFIG))
        return config.lookup(host);
        
    
    def __connectToHost(self, host):
        """
        This function returns a paramiko ssh client connected to the host 
        """
       
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        
        dataHost = self.__getDataHost(host);    
        
        client.connect(dataHost['hostname'], username=dataHost.get('user', None));
        
        #client.connect(dataHost['hostname'], username=dataHost['user'])
        
        return client

    def startProcess(self, ncpus=0):
        
        """
            LOCAL EXECUTION
        """
        if ncpus > 0:
            self.ncpus = ncpus
            return self.__ppJob()
        
        hosts = self.__getHosts()
        
        if len(hosts) == 1:
            """
                LOCAL EXECUTION
            """
            if hosts[0] == CONS.LOCALHOST:
                #print "detectado localhost en hostfile"
                self.ncpus = multiprocessing.cpu_count()
                return self.__ppJob()
        
        """
            CLOUD EXECUTION
        """
        
        #We start the Master Server
        master_server = self.__runMasterServer(hosts)
        
        #We calculate and put the data for the client in the masterserver queues
        self.__setInfoClients(master_server)
        
        #We start the clients
        self.__startClientsFromRemote(hosts)
        
               
        #We obtain the result of the clients
        qOut = master_server.getOutputQueue()
        NHosts = len(hosts)
        
        ret = 0
        if(NHosts > 0):
            ret =  qOut.get()
        
        i=1 
        while(i < NHosts):
            retAux = qOut.get()
            ret = self.merge(ret, retAux)
            i = i+1
        
        return ret
    
      
      
    def __getSortedHosts(self, hosts):
        """
        This function returns a list of hosts sorted by the number of cpus as well as the total number of cpus
        """  
        
        cpus = 0
        hostsInfo = []
        for host in hosts:
            hostCPU = self.__getCPUs(host)
            cpus = cpus + hostCPU
            hostsInfo.append([host,hostCPU])
             
        hostsInfoSorted = sorted(hostsInfo, key=lambda tupla: tupla[1], reverse=True) # Sort by #of CPUS in decreasing order
        
        return [hostsInfoSorted, cpus]
    
    
    def __runMasterServer(self, hosts):
        """
        This function starts the Colossus master server, and open a queue for each host in hosts
        Currently, the server is running in a specific IP and PORT. This should be parameterised.
        """
        
        for host in hosts:
            #print "HOST " + host
            self.remoteInputQueues[host] = multiprocessing.Queue()
            
        
        class JobQueueManager(SyncManager):
            pass

        JobQueueManager.register('getInputQueue', callable=lambda ip: self.remoteInputQueues[ip])
        JobQueueManager.register('getOutputQueue', callable=lambda: self.remoteResultQueue)
        
        IP_master = CONS.IPSERVER
        manager = JobQueueManager(address=(IP_master, CONS.PORT), authkey='test')
       
        
        manager.start()
        return manager
    
    
    def __setQueueInfo(self, manager, hostsInfoSorted, pairs, parts):
        """
        This function sets the values of index required to compute in the queues for each host
        """
        # We write the corresponding info to the queues
        currIndex = 0
        for hostInfo in hostsInfoSorted:
            hostname = hostInfo[0]
            ncpus = hostInfo[1]
            q = manager.getInputQueue(hostname)
            q.put(parts)                        # Put the parts
            q.put(pairs[currIndex][0])          # put the initial index for the host   
            if currIndex+ncpus-1 > len(pairs)-1:
                q.put(pairs[len(pairs)-1][1])
            else:   
                q.put(pairs[currIndex+ncpus-1][1])  # Put the end index for the host
            currIndex = currIndex + ncpus
   
    
    def __calculateNParts(self, total_cpus):
        """
        This function returns the increment to calculate the pairs of data given the total number of 
        available cpus
        """
        init = self.getInitialIndex()
        end = self.getFinalIndex()
        parts = (end-init+1) / total_cpus
        if parts <=0:
            parts = 1
        
        return parts
    
    def __computePairs(self, init, end, parts):
        """
        Computes the partitions to be computed by the workers
        """
        index = init
        pairs = []
        while(index <= end):
            init1 = index
            init2 = index+parts
            if init2 > end:
                init2=end
            
            pairs.append([init1,init2])
            index = init2+1
        return pairs
    
    
    def __setInfoClients(self, master_server):
        """
        In this function, the Colossus server, calculate the part, the pairs, and put this info into the 
        queues of the clients.
        """
        
        #Getting and ordering the hosts
        hosts = self.__getHosts()
        [hostsInfoSorted, total_cpus] = self.__getSortedHosts(hosts)
        
        # Now we calculate the parts:
        parts = self.__calculateNParts(total_cpus)

        # We compute the pairs        
        init = self.getInitialIndex()
        end = self.getFinalIndex() 
        pairs = self.__computePairs(init, end, parts)
        
        #We put the info in the queues of the master_server
        self.__setQueueInfo(master_server, hostsInfoSorted, pairs, parts)
                 
        return [master_server, hosts]
    
    
    def __runClient(self, host, command):
        """
        This function execute the command that starts a client on a remote machine
        """
        
        sshclient = self.__connectToHost(host);
        stdin, stdout, stderr = sshclient.exec_command(command)
        #print "STDOUT cliente"
        #print stdout.readlines()
        #print "STDERR cliente"
        #print stderr.readlines()
        
    
    def __startClientsFromRemote(self, hosts):
        """
        This functions is called by the Colossus main process, and start the clients in the machines specified in hosts
        """
        
        """
            CURRENT REMOTE VERSION
        """
        module = self.__module__
        theclass = self.__class__.__name__
        
        #We need to change it to the IP of the server
        ip = CONS.IPSERVER; 
        port = CONS.PORT;
        key = 'test';
        
        
        self.prepareClientData()
       
        thread_hosts = []
        for host in hosts:
            
            list_params = self.getCommandParameters()
            #print list_params
                   
            command = ' '.join([CONS.STARTCLIENT, module, theclass, ip, str(port), key] + list_params);
           
            t = multiprocessing.Process(target=self.__runClient, args=(host, command,)) 
            t.deamon = True
            thread_hosts.append(t)
            t.start()
        
        for thread in thread_hosts:
            thread.join()
            
  
    
    '''
    Client Side
    '''
    
    def __jobWorker(self, parts, init, end):
            
        index = init
        numThreads = 0
        threads = []
        while(index <= end):
            #print "Loops: ", elem
            init1 = index
            init2 = index+parts
            
            if init2 > end:
                init2=end
            
            ' We start the subprocesses' 
            t = multiprocessing.Process(target=self.__partial, args=(numThreads, init1, init2, )) 
            t.deamon = True
            threads.append(t)
            t.start()
            numThreads = numThreads + 1
            'jobsOut.append(job_server.submit(self.partial, (init1, init2, ), (),("abc","math",)))'
            #print "##### elapsed time submitting 1 job: ", time.time()-start_time    
            index = init2+1
        
        # We wait for all the subprocesses to end
        # TODO: Would it make any difference to process the partial solutions on the fly? check
        for thread in threads:
            thread.join()
            
        # Finally, we retrieve the results and merge them. 
        if (numThreads > 0):
            ret = self.resultQueue.get()
        i = 1
        
        while(i < numThreads):
            retAux = self.resultQueue.get()
            ret = self.merge(ret, retAux)
            i = i+1
            
        return ret
    
    
    def startClient(self, ip, port, authKey):
        
       
        manager = self.__startClientManager(ip, port, authKey)
        
        #Devuelve el nombre de la maquina
        myname = socket.gethostname()
        
        #inputQ = manager.getInputQueue(ip)  # Get the input queue corresponding to this Host
        inputQ = manager.getInputQueue(myname)  # Get the input queue corresponding to this Host
        outputQ = manager.getOutputQueue()  # Get the output queue
        
        parts = inputQ.get()                # Get the increment between batches
        init = inputQ.get()                 # Get the initial point
        end = inputQ.get()                  # Get the end point
        
        result = self.__jobWorker(parts, init, end)     # We execute the jobs
        
        outputQ.put(result)                             # We place the output to the remote queue
        return
    
    
    def __startClientManager(self,ip, port, authKey):
        """ 
        Create a manager for a client. This manager connects to a server on the
        given address and exposes the get_job_q and get_result_q methods for
        accessing the shared queues from the server.
        Return a manager object.
        """
        class ServerQueueManager(SyncManager):
            pass

        
        ServerQueueManager.register("getInputQueue")     # The Queue for receiving the execution parameters
        ServerQueueManager.register("getOutputQueue")    # The Queue for storing the results

        manager = ServerQueueManager(address=(ip, int(port)), authkey=authKey)
        manager.connect()

        #print 'Client connected to %s:%s' % (ip, port)
        return manager
    
    
    """
        FOR TESTING
    """  
    def getHosts(self):
        return self.__getHosts()
    
    def getDataHosts(self, host):
        return self.__getDataHost(host)
    
    def connecToHost(self, host):
        return self.__connectToHost(host)
    
    def getCPUs(self, host):
        return self.__getCPUs(host)
    
    def getSortedHosts(self, hosts):
        return self.__getSortedHosts(hosts)
    
    def getMasterServer(self, hosts):
        return self.__runMasterServer(hosts)
    
    def setInfoClients(self, master_server, hostsInfoSorted, pairs, parts):
        return self.__setQueueInfo(master_server, hostsInfoSorted, pairs, parts)
    
    def getPart(self, total_cpus):
        return self.__calculateNParts(total_cpus)
    
    def getPairs(self, init, end, parts):
        return self.__computePairs(init, end, parts)
        
    def getClientManager(self):
        return self.__startClientManager(ip='158.109.125.44', port = 8088, authKey='test')
