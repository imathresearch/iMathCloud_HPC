'''
Created on 14/02/2014

@author: andrea
'''

from HPC2.core.jobPython import JobPython
from HPC2.core.job import JobInfo
from urlparse import urlparse
from HPC2.exception.exceptions import HPC2Exception
from HPC2.common.util.jobUtils import JobUtils
import os
import unittest

class jobPython_Test(unittest.TestCase):


    def setUp(self):
        
        self.host = "127.0.0.1"
        self.port = "8080"
        self.filenamePath = "file://localhost/iMathCloud/ammartinez/TEST/test.py"
        self.namefile = "test"
        self.parameter = ""
        self.directoryPath = "file://localhost/iMathCloud/ammartinez/TEST"
        self.username = "ammartinez"
             
    def tearDown(self):
        pass

    #getters and setters
    def test_base(self):
        
        idJob = 1
        
        jobInf = JobInfo(idJob, self.host, self.port, self.filenamePath, self.directoryPath, self.parameter, self.username);
        jobP = JobPython(jobInf);
           
        file_out = str(idJob) + "_" + self.namefile + ".out"
        file_err = str(idJob) + "_" + self.namefile + ".err"  
        file_result = "result.csv"
        
        list_files = [file_out, file_err, file_result];
        jobP.setListOutputFiles(list_files)
            
        self.assertEqual(jobP.getIdJob(),idJob);
        self.assertEqual(jobP.getParameter(), self.parameter);
        self.assertEqual(jobP.getPort(), self.port);
        self.assertEqual(jobP.getSourceFile(), self.filenamePath);
        self.assertEqual(jobP.getUrl(), self.host);
        self.assertEqual(jobP.getPath(), self.directoryPath);       
        self.assertListEqual(list_files, jobP.getListOutputFiles());

    
    #name of stdout and stderr files
    def test_nameStdFiles(self):
        
        idJob = 2
             
        jobInf = JobInfo(idJob, self.host, self.port, self.filenamePath, self.directoryPath, self.parameter, self.username);
        jobP = JobPython(jobInf);
        
        jobP.execute();
        
        ju = JobUtils()
        user_root_dir = ju.getUserRootDir(self.username);
        
        original_code_to_execute = jobP.getPathNameSourceFile()
        user_absolute_path = os.path.dirname(original_code_to_execute).replace(user_root_dir, "");
        
        expected_file_out = user_absolute_path + "/" + str(idJob) + "_" + self.namefile + ".out";
        expected_file_err = user_absolute_path + "/" + str(idJob) + "_" + self.namefile + ".err";
        
        
        self.assertIn(expected_file_out, jobP.getListOutputFiles())
        self.assertIn(expected_file_err, jobP.getListOutputFiles());
    
       
    def test_contentStdFiles(self):
        
        idJob = 3
        
        jobInf = JobInfo(idJob, self.host, self.port, self.filenamePath, self.directoryPath, self.parameter, self.username);
        jobP = JobPython(jobInf);
        
        jobP.execute();
        
        std_files = jobP.getListOutputFiles();
        
        aux = urlparse(jobP.getSourceFile());
        name_Path = aux.path;
        directory = os.path.dirname(name_Path);
        
        ju = JobUtils()
        user_root_dir = ju.getUserRootDir(self.username);
        
        for file in std_files:
            f = open( user_root_dir + "/" + file, 'r');
            content = f.read();
            content = content.rstrip("\n");
            self.assertEqual(content, " 1 3 5 7 9 11 13 15 17 19 21 23 25");
            f.close();

    
    def test_SourceFileNotExist(self):
        
        idJob = 4
        #First, file does not exist
        uri_filenamePath = "file://localhost/iMathCloud/ammartinez/TEST/test1.py"
        
        jobInf = JobInfo(idJob, self.host, self.port, uri_filenamePath, self.directoryPath, self.parameter, self.username);
        jobP = JobPython(jobInf);
        
        jobP.execute();
        
        self.assertEqual(self.check_errorFile(jobP), 1);
        
    
    def test_DirectoryNotExist(self):
        
        idJob = 5
        #Second, dir does not exist, and therefore file.err does not exist
        uri_filenamePath = "file://localhost/iMathClou/TEST/test1.py"
        
        jobInf = JobInfo(idJob, self.host, self.port, uri_filenamePath, self.directoryPath, self.parameter, self.username);
        jobP = JobPython(jobInf);
        
        try:
            jobP.execute()
        except IOError, e:
            self.assertEqual("[Errno 2] No such file or directory: '/iMathClou/TEST/5_test1.out'", str(e));
            
              
    def test_ExtensionNotSupported(self):
        
        idJob = 6
        #Second, dir does not exist, and therefore file.err does not exist
        uri_filenamePath = "file://localhost/iMathCloud/TEST/extension.csv"
        
        jobInf = JobInfo(idJob, self.host, self.port, uri_filenamePath, self.directoryPath, self.parameter, self.username);
        jobP = JobPython(jobInf);
        
        try:
            jobP.execute();
            
        except HPC2Exception, e:
            self.assertEqual("('Unexpected error: ', 'Trying to execute a Non-Python file')", str(e));
           
    
    def check_errorFile(self, jobP):
        
        idJob = jobP.getIdJob()
        username = jobP.getUserName()
        
        ju = JobUtils()
        user_root_dir = ju.getUserRootDir(username);
        job_execution_dir = ju.getJobLocalExecutionDir(idJob, username)
            
        aux = urlparse(jobP.getSourceFile())
        name_Path = aux.path
        complete_execution_namepath = name_Path.replace(user_root_dir, job_execution_dir)
        
        directory = os.path.dirname(name_Path)
        name_ext = os.path.basename(name_Path)
        name, ext = os.path.splitext(name_ext)
        
        file_err = directory + "/" + str(jobP.getIdJob()) + "_" + name + ".err";
        print file_err     
        error_line = "python: can't open file '" + complete_execution_namepath + "': [Errno 2] No such file or directory"
         
        print error_line
        
        find = 0;
        try:
            f = open(file_err,'r');
            for linea in f:
                if linea.find(error_line) >= 0:
                    print "Encontrado: " + linea
                    find = 1
            
            f.close();     
        
        except IOError:
            print "El archivo indicado no existe"
            
        return find;
            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()