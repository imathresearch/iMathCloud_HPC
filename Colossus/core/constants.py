'''
Created on 11/11/2013

@author: iMath
'''

import os

def constant(f):
    '''
    Decorator to indicate that a property of a class is a constant, so, cannot be set, only get
    '''
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)


def deprecated(package="", instead=""):
    '''
    A decorator to indicate that the function or method called is deprecated. It calls anyway the function, but displays a message 
    in the console indicating it
    
    'package' is the optional package or class name where the deprecated function is called
    'instead' is the optional parameter containing the new function that should be called instead of the deprecated one 
    '''
    
    def wrap(f):
        def newF(*args, **kwargs):
            nameFunc = f.__name__
            part1=""
            part2=""
            if package!="":
                part1 = package + "."
            if instead!="":
                part2 = "Use " + package + "." + instead + " instead."
        
                print "Function " + part1 + nameFunc + " is deprecated. " + part2
            return f(*args, **kwargs)
        
        return newF
    return wrap

class CONS(object):
    '''
    It define the global constants for the Colossus core
    
    '''
    @constant
    def SSHCONFIG():
        return "/home/andrea/.ssh/config"
    
    @constant
    def VIRTUALENV():
        return "environments/virt2"
    
    @constant
    def IPSERVER():
        return "127.0.0.1"
    
    
    @constant
    def LOCALHOST():
        #return "127.0.0.1"
        return "localhost"    
    
    @constant
    def STARTCLIENT():
        C = CONS()
        s = ' '
        return s.join([C.PYTHONVIRTENV, C.STARTCLIENTSCRIPT])
    
    @constant
    def SHAREIMATHCLOUD():
        return "/mount_iMathCloud"
      
    @constant
    def VIRTUALENV_ABS():
        C = CONS();
        return os.path.join(C.SHAREIMATHCLOUD, C.VIRTUALENV)
    
    @constant
    def PYTHONVIRTENV():
        C = CONS()
        #path_to_pythonenv = "colossus/virt_env/virt1/bin/python"
        #return os.path.join(C.SHAREIMATHCLOUD, path_to_pythonenv);
        
        path_to_pythonenv = "bin/python"
        return os.path.join(C.VIRTUALENV_ABS, path_to_pythonenv);
        #return "/iMathCloud/colossus/virt_env/virt1/bin/python"
    
    @constant
    def HOSTFILE():
        C = CONS()
        #path_hostfile = "colossus/host_file.txt"
        #return os.path.join(C.SHAREIMATHCLOUD, path_hostfile);
        
        path_hostfile = "etc/host_file.txt"
        return os.path.join(C.VIRTUALENV_ABS, path_hostfile);
    
    @constant
    def STARTCLIENTSCRIPT():
        C = CONS()
        #path_to_startClientscript = "colossus/exec_startClient.py"
        #return os.path.join(C.SHAREIMATHCLOUD,path_to_startClientscript)
        
        path_to_startClientscript = "etc/exec_startClient.py"
        return os.path.join(C.VIRTUALENV_ABS, path_to_startClientscript);
     
    @constant
    def FILECLIENTDATA():
        C = CONS()
        path_to_fileclientdata = "data/data.txt"
        return os.path.join(C.SHAREIMATHCLOUD,path_to_fileclientdata)

    @constant
    def PORT():
        return 8088
    
    @constant
    def BEGINTOKEN():
        return "###---###\n"
    
    @constant
    def ENDTOKEN():
        return "---###---\n"
    
    @constant
    def BEGINTOKEN_MERGE():
        return "###MERGE###\n"
    
    @constant
    def ENDTOKEN_MERGE():
        return "---MERGE---\n"
    
    @constant
    def BEGINTOKEN_PROCESSELEM():
        return "###PROCESSELEM###\n"
    
    @constant
    def ENDTOKEN_PROCESSELEM():
        return "---PROCESSELEM---\n"
    
    @constant
    def ENDPROCESS():
        return "---------\n"
    
    @constant
    def PATH_TEMP_FILES():
        C = CONS();
        return os.path.join(C.SHAREIMATHCLOUD, "temp");
        