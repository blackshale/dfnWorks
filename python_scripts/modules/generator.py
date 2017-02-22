import os
import sys
import shutil
from time import time
import helper

def dfnGen(self):
    ''' Run the dfnGen workflow. 
    1) make_working_directory: Create a directory with name of job
    2) check_input: Check input parameters and create a clean version of the input file
    3) create_network: Create network. DFNGEN v2.0 is called and creates the network
    4) output_report: Generate a PDF summary of the DFN generation
    5) mesh_network: calls module dfnGen_meshing and runs LaGriT to mesh the DFN
    '''
    tic_gen = time()
    # Create Working directory
    tic = time()
    self.make_working_directory()
    #helper.dump_time(self._jobname, 'Function: make_working_directory', time()- tic) 

    # Check input file  
    tic = time()
    self.check_input()
    #helper.dump_time(self._jobname, 'Function: check_input', time() - tic)   

    # Create network    
    tic = time()
    self.create_network()
    #helper.dump_time(self._jobname, 'Function: create_network', time() - tic)    
    
    tic = time()
    self.output_report()
    #helper.dump_time(self._jobname, 'output_report', time() - tic)   

    # Mesh Network
    tic = time()
    self.mesh_network()
    #helper.dump_time(self._jobname, 'Function: mesh_network', time() - tic)  
    print ('='*80)
    print 'dfnGen Complete'
    print ('='*80)
    print ''
    #helper.dump_time(self._jobname, 'Process: dfnGen',time() - tic_gen)  

def make_working_directory(self):
    '''
    make working directories for fracture generation
    '''    

    try:
        os.mkdir(self._jobname)
    except OSError:
        print '\nFolder ', self._jobname, ' exists'
        keep = raw_input('Do you want to delete it? [yes/no] \n')
        if keep == 'yes' or keep == 'y':
            print 'Deleting', self._jobname 
            shutil.rmtree(self._jobname)
            print 'Creating', self._jobname 
            os.mkdir(self._jobname)    
        elif keep == 'no' or 'n':
            sys.exit("Not deleting folder. Exiting Program") 
        else:
            sys.exit("Unknown Response. Exiting Program") 
    os.mkdir(self._jobname + '/radii')
    os.mkdir(self._jobname + '/intersections')
    os.mkdir(self._jobname + '/polys')
    os.chdir(self._jobname)
    cwd = os.getcwd()
    print("Current directory is now: %s\n"%cwd)
    print "Jobname is ", self._jobname   

def create_network(self):
    print '--> Running DFNGEN'    
    # copy input file into job folder    
    os.system(os.environ['DFNGEN_PATH']+'/./DFNGen ' + self._local_dfnGen_file[:-4] + '_clean.dat' + ' ' + self._jobname )

    if os.path.isfile("params.txt") is False:
        print '--> Generation Failed'
        print '--> Exiting Program'
        exit()
    else:
        print('-'*80)
        print("Generation Succeeded")
        print('-'*80)
