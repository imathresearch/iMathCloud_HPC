# (C) 2013 iMath Research S.L. - All rights reserved.
""" Implements the class JobController, which is in charge of executing the 
job in the current host and 

Authors:

@author iMath
"""

from HPC2.common.util.WebService import WebServiceClass
from HPC2.common.util.json import JSON
from HPC2.common.constants import CONS

from HPC2.core.jobPython import JobPython
from HPC2.core.jobPlugin import JobPlugin

from HPC2.common.util.jobUtils import JobUtils


CONS=CONS()

class JobController(object):
    '''
    Creation:
        JobController(job) 
            job: Class Job from Colossus.core.job
    '''
    job = None
    
    def __init__(self, job):
        self.job = job
    
    def start(self):
        self.getJob().execute()
        self.__finalization()
    
    def done(self, status):
        #TODO: 
        print "Done"
    
    def getJob(self):
        return self.job
    
    def __finalization(self):
        
        jsonClass = JSON()
        listOutputDirs = self.getJob().getListOutputDirs()
        webService = WebServiceClass()
        urlHost = self.getJob().getUrl()
        portHost = self.getJob().getPort()
        idJob = self.getJob().getIdJob()
        
        if isinstance(self.getJob(), JobPython):
            listOutputFiles = self.getJob().getListOutputFiles()
            jsonString = jsonClass.FilesDirsPlusPathtoJSonString(listOutputFiles, listOutputDirs)
            listResults = jsonClass.JSonStringToJsonDecoder(jsonString)  
            url = CONS.HTTP + urlHost + ':' + portHost + CONS.RESULTRESPJOBPYTHON + '/' + idJob + '/'
            webService.callWebServiceJSON(url,listResults)  
        
        elif isinstance(self.getJob(), JobPlugin):                       
            #JobPlugin output files, do not have the complete path
            #So we need to complete the name of the file, with the complete path
            #from the root of the user
            ju = JobUtils();
            ju.setAbsolutePathJobOutputFiles(self.getJob());
            listOutputFiles = self.getJob().getListOutputFiles();                  
            
            jsonString = jsonClass.FilesDirsPlusPathtoJSonString(listOutputFiles, listOutputDirs)
            listResults = jsonClass.JSonStringToJsonDecoder(jsonString)  
            url = CONS.HTTP + urlHost + ':' + portHost + CONS.RESULTRESP + '/' + idJob + '/'
            webService.callWebServiceJSON(url,listResults)            
            #listResults = jsonClass.ArrayToJsonFileNames(listOutputFiles)
            #url = CONS.HTTP + urlHost + ':' + portHost + CONS.RESULTRESP + '/' + idJob + '/'
            #webService.callWebServiceJSON(url,listResults)  
    
        return 0