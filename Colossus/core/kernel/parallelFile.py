'''
Created on 26/03/2014

@author: andrea
'''
import pickle
from Colossus.core.kernel.parallelListPair import ParallelListPairExtended

class ParallelFile(ParallelListPairExtended):
    '''
    classdocs
    '''
    def __init__(self, data_or_filename, *args, **kwargs):
        '''
        Constructor
        '''
        data = None
        if isinstance(data_or_filename, str):
            data =  pickle.load( open(data_or_filename, "rb" ) )
        else:
            data = data_or_filename
        
        return super(ParallelFile, self).__init__(data, *args, **kwargs)
