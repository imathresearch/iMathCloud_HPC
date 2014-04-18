# (C) 2013 iMath Research S.L. - All rights reserved.

""" The handlers for core services of Colossus

Authors:

* ipinyol
"""

#import tornado.ioloop
import tornado.web
from Colossus.core.job import JobInfo
from Colossus.core.jobPython import JobPython
from Colossus.core.jobController import JobController
 
class SubmitHandler(tornado.web.RequestHandler):

    def post(self):

        host = self.get_argument("host",None)
        port = self.get_argument("port",None)
        idJob = self.get_argument("id",None)        
        filenamePath = self.get_argument("fileName",None)
        parameter = self.get_argument("parameter",None)
        directoryPath = self.get_argument("directory",None)
        jobInf = JobInfo(idJob,host, port, filenamePath, directoryPath, parameter)
        job = JobPython(jobInf);
        jobController = JobController(job)
        jobController.start()
        return 0
