'''
Created on 12/12/2013

@author: iMath
'''
import abc
from job import Job

class JobPlugin(Job):
    '''
    Extends:
        Class Job from HPC2.core.job
    
    All plugins must extend this class  
    '''
    __metaclass__ = abc.ABCMeta
    
    function = None     # The function name
    plugin = None       # The plugin name
    def __init__(self, jobInfo=None):
        super(JobPlugin,self).__init__(jobInfo)

    def setPlugin(self, plugin):
        self.plugin = plugin
    
    def getPlugin(self):
        return self.plugin
    
    def setFunction(self,function):
        self.function = function
    
    def getFunction(self):
        return self.function
    
    @abc.abstractmethod
    def execute(self):
        """Abstract method to be implemented in one of the subclases
        Must return 0 if everything was OK. 1 if error. Must be a synchronous call in the current version
        """
        return