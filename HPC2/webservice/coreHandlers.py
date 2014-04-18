# (C) 2013 iMath Research S.L. - All rights reserved.

""" The handlers for core services of Colossus

Authors:

* iMath
"""

#import tornado.ioloop
import tornado.web
import importlib
import multiprocessing


from HPC2.core.job import JobInfo
from HPC2.core.jobPython import JobPython
from HPC2.core.jobController import JobController
from HPC2.core.jobMonitor import JobMonitor 
from HPC2.common.constants import CONS
from HPC2.common.util.jobUtils import JobUtils
from urlparse import urlparse

CONS = CONS()

class SubmitHandler(tornado.web.RequestHandler):

    def get(self):

        host = self.get_argument("host",None)
        port = self.get_argument("port",None)
        idJob = self.get_argument("id",None)        
        filenamePath = self.get_argument("fileName",None)
        parameter = self.get_argument("parameter",None)
        directoryPath = self.get_argument("directory",None)
        
        ju = JobUtils();
        user = ju.getUserName(urlparse(directoryPath).path);
      
        jobInf = JobInfo(idJob,host, port, filenamePath, directoryPath, parameter, user)
        job = JobPython(jobInf);
        jobController = JobController(job)
        jobController.start()
        
        #print "*****FIN DEL JOBCONTROLLER"
        #return 0

class PluginHandler(tornado.web.RequestHandler):
    
    def get(self):
        t = multiprocessing.Process(target=self.__asyncPluginHandler, args=()) 
        t.deamon = True
        t.start()
        #return 0
    
    def __asyncPluginHandler(self):
        host = self.get_argument("host",None)
        port = self.get_argument("port",None)
        idJob = self.get_argument("id",None)        
        filenamePath = self.get_argument("fileName",None)
        parameter = self.get_argument("parameter",None)
        directoryPath = self.get_argument("directory",None)
        plugin = self.get_argument("plugin",None)
        function = self.get_argument("function",None)
        
        ju = JobUtils();
        user = ju.getUserName(urlparse(directoryPath).path);
        
        jobInf = JobInfo(idJob,host, port, filenamePath, directoryPath, parameter, user)
        
        fullName = CONS.PLUGINNAME + "." + plugin + "." + CONS.MAINPLUGIN
        moduleMain = importlib.import_module(fullName)
        job = moduleMain.getJobInstance()
        job.setJobInfo(jobInf)
        job.setPlugin(plugin)
        job.setFunction(function)
        jobController = JobController(job)
        jobController.start()
        
class PCTHandler(tornado.web.RequestHandler):
    def get(self):
        idJob = self.get_argument("id",None)
        if idJob==None:
            self.send_error(500,"ifJob Must be informed")
            return 0
        
        #print "After if"
        jobMonitor = JobMonitor(idJob)
        
        #listStr = jobMonitor.getPercentages()
        
        #listStr = jobMonitor.getPercentagesMultiMachines();

        listStr = []
        jsonOut = dict(perc = listStr)
        self.write(jsonOut)             # According to documentation, RequestHandler.write convert to json the variable structure if it is a dict
        self.flush()
        self.finish()
        #return 0
        
        