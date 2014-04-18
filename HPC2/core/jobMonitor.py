''' Implements the class JobMonitor, which is in charge of returning the percentage of completion of the Job 

Created on 08/01/2014

@author: iMath
'''
import paramiko
import multiprocessing
from Colossus.core.constants import CONS        # Colossus constants to retrieve 

CONS=CONS()

class JobMonitor(object):
    
    idJob = None
    
    def __init__(self, idJob):
        self.idJob = idJob
        
    def __getHosts(self):
        
        list_IP = [];
        IPs=(l.rstrip('\n') for l in file(CONS.HOSTFILE,"Ur"));
        for ip in IPs:
            list_IP.append(ip);

        return list_IP;
    
    def __getCPUs(self, host):
        
        if (host== CONS.LOCALHOST):    # The local host
            return multiprocessing.cpu_count()
        else:
            sshclient = self.__connectToHost(host);
            stdin, stdout, stderr = sshclient.exec_command('grep processor /proc/cpuinfo')
        
            return len(stdout.readlines())
         
        return 1
    
    def __getDataHost(self, host):
          # ssh config file
        config = paramiko.SSHConfig()
        config.parse(open(CONS.SSHCONFIG))
        #print "host " + host
        #print config.lookup(host);
        return config.lookup(host);
        
    
    def __connectToHost(self, host):
       
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        
        dataHost = self.__getDataHost(host);
        
        #print "DATAHOST "
        #print dataHost  
        
        client.connect(dataHost['hostname'], username=dataHost['user'])
        
        return client
    
    
    def getPercentages(self):
        pers = []
        if (self.idJob != None):
            done = False
            i = 0
            while not done:
                fullPathName = self.__getFullPathName(i)
                try:
                    fd = open(fullPathName, "r")
                    numStr = fd.read()
                    pers = pers + [numStr.strip()]
                    fd.close()
                    i = i + 1
                except:
                    done = True
        
        return pers
    
    def getPercentagesMultiMachines(self):
        pers = []
        if (self.idJob != None):
            done = False
            i = 0      
            hosts = self.__getHosts();
            for host in hosts:
                cpus = self.__getCPUs(host);             
                for x in range(0, cpus):
                    fullPathName = self.__getFullPathName(host, i)
                    fd = open(fullPathName, "r")
                    numStr = fd.read()
                    pers = pers + [numStr.strip()]
                    fd.close()
                    i = i + 1
            
        return pers
            
    
    def __getFullPathName(self, host, num):
        name = ""
        #print "id job " + str(self.idJob)
        #print "num thread " + str(num)
        if self.idJob!=None:
            name = CONS.PATH_TEMP_FILES + host + "_" + str(self.idJob) + "_" + str(num)
            #print name
            
        return name