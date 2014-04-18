# (C) 2013 iMath Research S.L. - All rights reserved.
""" Implements the class JobController, which is in charge of executing the 
job in the current host and 

Authors:

@author ipinyol
"""
from Colossus.core.job import Job
import threading 

class JobController(object):
    '''
    Creation:
        JobController(job) 
            job: Class Job from Colossus.core.job
    '''
    def __init__(self, job):
        self.jobThread = JobThread(self);
        self.job = job
    
    def start(self):
        self.jobThread.start();
    
    def done(self, status):
        #TODO: 
        #print "Done"
    
    def getJob(self):
        return self.job
        

class JobThread(threading.Thread):
    def __init__(self, jobController):  
        threading.Thread.__init__(self)  
        self.jobController = jobController
  
    def run(self):  
        self.jobController.getJob().executeJob()
        self.jobController.done("OK")
