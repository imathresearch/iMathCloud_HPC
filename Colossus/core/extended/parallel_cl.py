'''
Created on Nov 14, 2013

It contains the classes that use Colossus parallel Classes where abstract methods are called
from comand line executable programs

@author: iMath
'''

import subprocess
import time
from Colossus.core.kernel.parallelListPair import ParallelListPair
from Colossus.core.kernel.parallelListPair import ParallelListPairExtended
from Colossus.core.constants import CONS

CONS = CONS()

def trim(str):
    if (str[len(str)-1]=='\n'):
        return str[0:len(str)-1]
    return str

class ParallelListPairExtendedCL(ParallelListPairExtended):
    '''
    Implements the ParallelListPair class with the functionality of calling its abstract methods 
    from command-line executable file where the result is issued in the standard output and the communication
    through pipes 
    '''
    
    def __init__(self, data, func_processElement, func_merge):
        
        super(ParallelListPairCL,self).__init__(data, processElementExternal=func_processElement, mergeExternal=func_merge)
        #self.func_processElement = func_processElement
        #self.func_merge = func_merge
    
    def processElement(self, inp, id=None):
        
        fileIndex = inp[0]
        i0 = inp[1]
        i1 = inp[2]
        #call = self.func_processElement + " " + str(i0) + " " + str(i1)
        #call = self.func_processElement + ' ' + str(i0) + ' ' + str(i1)
        #print call
        #process = subprocess.Popen(call, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        token = str(i0) + '\n' + str(i1) + '\n' + str(self.data[i0])+'\n'+str(self.data[i1])+ '\n'
        token = CONS.BEGINTOKEN_PROCESSELEM + token + CONS.ENDTOKEN_PROCESSELEM
        #print token
        start_time = time.time()
        self.processElementExternal_subs[id].stdin.write(token)
        #print "elapsed time: ", time.time()-start_time
        #out = subprocess.check_output(call, shell=True)
        out = self.processElementExternal_subs[id].stdout.readline()
        #out = "hola"
        return trim(out)
    
    def merge(self,out1, out2, id=None):
        #self.mergeExternal_subs[id].stdin.write(CONS.BEGINTOKEN+"HOLAAAAAAAAAAAAA+\n")
        #call = self.func_merge + ' "'  + out1 + '" "'  + out2 + '"'
        #print call
        token = trim(out1) + '\n' + trim(out2) + '\n'
        token = CONS.BEGINTOKEN_MERGE + token + CONS.ENDTOKEN_MERGE
        #out = subprocess.check_output(call, shell=True)
        #if (id == -1):
        #    print "merging:"+token
        self.mergeExternal_subs[id].stdin.write(token)
        out = self.mergeExternal_subs[id].stdout.readline()
        #out = "merge"
        return trim(out)

class ParallelListPairCL(ParallelListPair):
    '''
    Implements the ParallelListPair class with the functionality of calling its abstract methods 
    from command-line executable file where the result is issued in the standard output and the communication
    through pipes 
    '''
    
    def __init__(self, data, func_processElement, func_merge):
        
        super(ParallelListPairCL,self).__init__(data, processElementExternal=func_processElement, mergeExternal=func_merge)
        #self.func_processElement = func_processElement
        #self.func_merge = func_merge
    
    def processElement(self, inp, id=None):
        
        i0 = inp[0]
        i1 = inp[1]
        #call = self.func_processElement + " " + str(i0) + " " + str(i1)
        #call = self.func_processElement + ' ' + str(i0) + ' ' + str(i1)
        #print call
        #process = subprocess.Popen(call, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        token = str(i0) + '\n' + str(i1) + '\n' + str(self.data[i0])+'\n'+str(self.data[i1])+ '\n'
        token = CONS.BEGINTOKEN_PROCESSELEM + token + CONS.ENDTOKEN_PROCESSELEM
        #print token
        start_time = time.time()
        self.processElementExternal_subs[id].stdin.write(token)
        #print "elapsed time: ", time.time()-start_time
        #out = subprocess.check_output(call, shell=True)
        out = self.processElementExternal_subs[id].stdout.readline()
        #out = "hola"
        return trim(out)
    
    def merge(self,out1, out2, id=None):
        #self.mergeExternal_subs[id].stdin.write(CONS.BEGINTOKEN+"HOLAAAAAAAAAAAAA+\n")
        #call = self.func_merge + ' "'  + out1 + '" "'  + out2 + '"'
        #print call
        token = trim(out1) + '\n' + trim(out2) + '\n'
        token = CONS.BEGINTOKEN_MERGE + token + CONS.ENDTOKEN_MERGE
        #out = subprocess.check_output(call, shell=True)
        #if (id == -1):
        #    print "merging:"+token
        self.mergeExternal_subs[id].stdin.write(token)
        out = self.mergeExternal_subs[id].stdout.readline()
        #out = "merge"
        return trim(out)
    
    def getCommandParameters(self):
        pass
    
    def prepareClientData(self):
        pass
        