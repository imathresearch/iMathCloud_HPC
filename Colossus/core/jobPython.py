# (C) 2013 iMath Research S.L. - All rights reserved.

""" Implements the class JobPython, a sub class of the class Job

Authors:

@author iMath
"""
import imp
import os

from job import Job
from Colossus.exception.exceptions import ColossusException

class JobPython(Job):
    '''
    Extends:
        Class Job from Colossus.core.job
    Creation:
        JobPython(jobInfo) 
            jobInfo: Class JobInfo from Colossus.core.job
    '''
    
    def __init__(self, jobInfo):
        super(JobPython,self).__init__(jobInfo)

    def executeJob(self):
        try:
            mod_name,file_ext = os.path.splitext(os.path.split(self.getSourceFile())[-1])

            if file_ext.lower() == '.py':
                imp.load_source(mod_name, self.getSourceFile())
                
            elif file_ext.lower() == '.pyc':
                imp.load_compiled(mod_name, self.getSourceFile())
        
            else:
                msg = "Unexpected error: ", "Trying to execute a Non-Python file"
                raise ColossusException(msg)
        except:
            raise
        return 1