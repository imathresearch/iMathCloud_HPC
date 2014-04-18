'''
Created on 12/12/2013

@author: iMath
'''
from HPC2.plugin.stat.jobStat import JobStat

'''
Mandatory plugin function
'''
def getJobInstance():
    return JobStat()
    
