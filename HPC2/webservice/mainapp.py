# (C) 2013 iMath Research S.L. - All rights reserved.

""" The tornado-based module for iMathCloud restful connectivity

Authors:

* iMath
"""

import tornado.ioloop
import tornado.web

from HPC2.webservice.coreHandlers import SubmitHandler
from HPC2.webservice.coreHandlers import PluginHandler
from HPC2.webservice.coreHandlers import PCTHandler


application = tornado.web.Application([
    (r"/core/submit", SubmitHandler),
    (r"/plugin", PluginHandler),
    (r"/getpct", PCTHandler)
])

if __name__ == "__main__":
    application.listen(8890,address='')
    tornado.ioloop.IOLoop.instance().start()
