# (C) 2013 iMath Research S.L. - All rights reserved.

""" The tornado-based module for iMathCloud restful connectivity

Authors:

* ipinyol
"""

import tornado.ioloop.IOLoop
import tornado.web.Application

from coreHandlers import SubmitHandler


application = tornado.web.Application([
    (r"/core/submit", SubmitHandler)
])

if __name__ == "__main__":
    application.listen(8890,address='')
    tornado.ioloop.IOLoop.instance().start()
