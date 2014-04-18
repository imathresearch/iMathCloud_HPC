'''
Created on 25/03/2014

@author: andrea
'''
import abc
from Colossus.exception.exceptions import ColossusException
from Colossus.core.kernel.parallel_gen import ParallelGen

from pymongo import MongoClient

class ParallelMongo(ParallelGen):
    '''
    classdocs
    '''

    def __init__(self, database, collection, ip, port):
        
        self.database = database
        self.collection = collection
        self.ip = ip
        self.port = port
        
        self.mongo_client = MongoClient(self.ip, int(self.port))
        
        #print "Connected to database " + database + " at IP " + ip + " in port " + str(port)
        
        self.db = self.mongo_client[self.database]
        self.col = self.db[self.collection]
        self.index_cursor = self.col.find({}, {'_id':1}).sort('_id',1)
        
    
    def getInitialIndex(self):
        return 0
    
    def getFinalIndex(self):
        return self.index_cursor.count()-1;
    
    def getNextIndex(self, i):
        if i < 0:
            raise ColossusException("ParallelMongo.getNextIndex - Index out of lower bounds: Minimum is 0, but asked for the next of "+ str(i))
        if i>=self.getFinalIndex():
            raise ColossusException("ParallelMongo.getNextIndex  - Index out of upper bounds: Maximum is " + str(self.getFinalIndex()) + ", but asked for the next of " + str(i))
        return i+1;
    
    def getElement(self, i):
        elem = self.index_cursor[i]
        return self.col.find_one(elem);
    
    @abc.abstractmethod
    def processElement(self, x, id=None):
        return 

    @abc.abstractmethod
    def merge(self, out1, out2, id=None):
        return
    
    def getCommandParameters(self):
       
        return [self.database, self.collection, str(self.ip), str(self.port)]
        
    
    def prepareClientData(self):
        pass
    
    def writeToDB(self, document, database, collection, ip, port):
        """
            Function that represents the MongoDB link for writing
        """
        mongo_client = MongoClient(ip, int(port))
        db = mongo_client[database]
        col = db[collection]
        col.insert(document)
    
    