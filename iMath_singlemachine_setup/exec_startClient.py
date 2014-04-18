import sys
import numpy
import os
import pickle



module_name = sys.argv[1]
class_name = sys.argv[2]

b= module_name.split('.')
b.pop();
parent_name = '.'.join(b)

print module_name
print parent_name
print class_name

try:
        colossus_subclass = getattr(__import__(module_name, fromlist=[parent_name]), class_name)
except ImportError, exception:
        print "Could not find module: {0}".format(sys.argv[1])
        quit()


print sys.argv[6:]
colossus_subclass(*sys.argv[6:]).startClient(sys.argv[3], sys.argv[4], sys.argv[5])

