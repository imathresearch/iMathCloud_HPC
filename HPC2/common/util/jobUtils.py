# (C) 2014 iMath Research S.L. - All rights reserved.
'''
Created on 18/02/2014

This class offers several services required to execute a python job

@author: andrea
'''

import re
import os

from HPC2.common.constants import CONS
from HPC2.exception.exceptions import HPC2Exception

CONS=CONS()

class JobUtils(object):
    
    '''
        Return the local execution dir of a job (idjob) belongs to a user (username)
        The params idjob and username are required to create in the correct location the execution dir
    '''
    def getJobLocalExecutionDir(self, idjob, username):
        
        j = 'job' + str(idjob)
        #return os.path.join(path , j)
        #return os.path.join(CONS.EXECUTION_DIR(), username, j)
        return os.path.join(CONS.EXECUTION_DIR, username, j)
    
    '''
        Return the user root dir of a username
        user_root_dir = OUR_ROOT_FILE_SYSTEMA + username
    '''
    def getUserRootDir(self, username):
        
        #return CONS.ROOT_FILE_SYSTEM + "/" + username
        return os.path.join(CONS.ROOT_FILE_SYSTEM, username)
    
    '''
        Return the username of the user associated to a job
        In HPC2 we do not the user characteristics, but we need to know the username to create and work correctly with his directory execution
    '''
    def getUserName(self, path_from_root):
        
        try:
          
            #First it is necesary to check that the root system file is contained in the path_from_root
            check = path_from_root[0:len(CONS.ROOT_FILE_SYSTEM)]

            if check == CONS.ROOT_FILE_SYSTEM:       
                relPath = path_from_root[len((CONS.ROOT_FILE_SYSTEM).rstrip('/'))+1:];
                user = relPath.split('/')[0];
                return user
           
            else:
                msg = "Unexpected error: ", "Path from root does not contain the path of the root system file"
                raise HPC2Exception(msg)
            
        except:
            raise
    
    '''
        Return the real execution dir of a job (in the system file of iMathCloud that belongs to the user)
    '''
    def getJobRealExecutionDir(self, job):
     
        pathName_sf = job.getPathNameSourceFile();
        #We supposse that the execution dir is the same where the source file reside and the same where the new files are generated
        #We obtain the absolute path from the root file system of iMathCloud
        execution_dir = os.path.dirname(pathName_sf);
        # We obtain the user root dir from the root file system of iMathclou 
        user_root_dir = self.getUserRootDir(job.getUserName()); 
        #print "execution dir " + execution_dir
        #We need the absolute path from the point of view of the user ROOT
        if user_root_dir != execution_dir:
            user_execution_dir = execution_dir.replace(user_root_dir, "");
        else:
            #else means that the job is executed in the user root directory
            user_execution_dir = execution_dir.replace(user_root_dir, "/");
            
        return user_execution_dir
    
    '''
        Given a list of output files of a job characterised by files that only contain their names
        this function modify this list by completing the name of each file with the complete path
        In this case the complete path is taking from the path of the job source file
        Now, this function is ONLY used in the case of JobPlugin, in which all the output files are generated
        without path. 
    '''
    
    def setAbsolutePathJobOutputFiles(self, job):
        
        list_files = job.getListOutputFiles();
        new_list = []
        execution_dir = self.getJobRealExecutionDir(job)
        for file in list_files:
            new_list.append(os.path.join(execution_dir, file));
        
        print "New list of output files: "
        print new_list
            
        job.setListOutputFiles(new_list);
        
        
    '''
        This function copies the a directory tree of the user to the job execution directory.
        We use it in jobPython.py to copy the complete directory tree of the user (from the ROOT) to the job execution directory
        The files are not a real copy, are a symbolic link to the real file in the user file system
    '''
    def copyUserDirToJobDir(self, user_dir, job_dir):
        
        os.mkdir(job_dir)
        os.chdir(job_dir)

        for dirName, subdirList, fileList in os.walk(user_dir):

            new_dir = dirName.replace(user_dir,'.');

            if new_dir != '.':
                os.mkdir(new_dir)

            for f in fileList:
                os.symlink(os.path.join(dirName, f), os.path.join(new_dir, f))

    '''
        Return a dictionary that contains a "photo" of the state of a specific directory
        A photo means that we store as a dictionary the tree directory below dir
    '''
    def snapshotDir(self, dir):
    
        directory = dir
        ss = {}
        for root, dirs, files in os.walk(directory):
           
            rel = root.replace(directory, '').lstrip('/') 
            cur = ss
           
            if len(rel) > 0:
                for d in rel.split('/'):
                    cur = cur[d]
            
            for d in dirs:
                cur[d] = {}
                
            for f in files:
                cur[f] = None

        return ss
    
    '''
        This function compares a snapshot of a directory with a real dir
        This function is used to detect the new files and directories created after the execution of a job.
        So, before a job is executed:
        1. Take a snapshot of the complete directory tree of the user
        2. Copy this directory to the execution dir of the job
        3. Execute the job
        After the job has finished:
        1. Compare the execution dir of the job with the previosly taken snapshot.
        
        This function returns:
        a) new files and directories to copy to the user file system
        b) new files and directories to return as an output of the job
        
        a is a subset of b, because if nested directories or files are created, we only return the top. However, in the b set 
        we have to return everything new to be correctly created in the database of iMathCloud
    '''
    def compareSnapshotDir(self, snapshot, dir):
        
        ss = snapshot
              
        tocopy_files = [ ]
        tocopy_dirs = []
        toDB_files = []
        toDB_dirs = []
        
        for root, dirs, files in os.walk(dir):
         
            rel = root.replace(dir, '').lstrip('/')
            cur = ss
            
            if len(rel) > 0:
                rel_exists = True
                for d in rel.split('/'):
                    #print "Rel split: " 
                    #print rel.split('/')
                    if d not in cur:
                        #print "D " + d
                        rel_exists = False
                        continue
                    cur = cur[d]
                if rel_exists is False:
                    for d in dirs:
                        toDB_dirs.append(os.path.join(rel, d))
                    for f in files:             
                        toDB_files.append(os.path.join(rel, f))
                    continue

            for d in dirs:
                if d not in cur:
                    tocopy_dirs.append(os.path.join(rel, d))
                    toDB_dirs.append(os.path.join(rel, d))
            for f in files:
                if f not in cur:
                    tocopy_files.append(os.path.join(rel, f))
                    toDB_files.append(os.path.join(rel, f))
        
        #print "to copy"
        #print tocopy_files
        #print tocopy_dirs
        
        #print "to db"
        #print toDB_files
        #print toDB_dirs

        return [tocopy_files, tocopy_dirs, toDB_files, toDB_dirs] 
