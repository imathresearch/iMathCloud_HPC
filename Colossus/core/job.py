# (C) 2013 iMath Research S.L. - All rights reserved.

""" The module that implements an abstract Job, which must be instantiated as 
PythonJob, RJob, etc...

Authors:

@author ipinyol
"""

import abc

class JobInfo(object):
    
    def __init__(self, idJob=None, url=None, port=None, sourceFile=None, path=None, parameter=None):
        self.idJob = idJob
        self.url = url
        self.port = port
        self.sourceFile = sourceFile
        self.path = path
        self.parameter = parameter
    
class Job(object): 
    '''
    Creation:
        Job(jobInfo) 
            jobInfo: Class JobINfo from Colossus.core.job
    '''
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, jobInfo):
        self.jobInfo = jobInfo
        
    def getIdJob(self):
        return self.jobInfo.idJob
    
    def getUrl(self):
        return self.jobInfo.url
    
    def getPort(self):
        return self.jobInfo.port
    
    def getSourceFile(self):
        return self.jobInfo.sourceFile
    
    def getPath(self):
        return self.jobInfo.path
    
    def submit(self):
        self.prepareSubmission()
        self.status =  self.executeJob()
        self.informFinalization()
    
    def prepareSubmission(self):
        return
    
    def informFinalization(self):
        return 
        
    @abc.abstractmethod
    def executeJob(self):
        """Abstract method to be implemented in one of the subclases
        Must return 0 if everything was OK. 1 if error. Must be a synchronous call in the current version
        """
        return