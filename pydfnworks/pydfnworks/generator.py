import os
import sys
import shutil
from time import time
import subprocess

def dfn_gen(self,output=True):
    ''' Wrapper script the runs the dfnGen workflow.     
    Run the dfnGen workflow: 
        * 1) make_working_directory: Create a directory with name of job
        * 2) check_input: Check input parameters and create a clean version of the input file
        * 3) create_network: Create network. DFNGEN v2.0 is called and creates the network
        * 4) output_report: Generate a PDF summary of the DFN generation
        * 5) mesh_network: calls module dfnGen_meshing and runs LaGriT to mesh the DFN

    Parameters
    ----------
    DFN Class
    output (bool): If True, output pdf will be created. If False, no pdf is made 

    Returns
    -------
    None

    Notes
    -----
    Details of each portion of the routine are in those sections

    '''
    tic_gen = time()
    # Create Working directory
    tic = time()
    self.make_working_directory()
    self.dump_time('Function: make_working_directory', time()- tic) 
    
    # Check input file  
    tic = time()
    self.check_input()
    self.dump_time('Function: check_input', time() - tic)   

    # Create network    
    tic = time()
    self.create_network()
    self.dump_time('Function: create_network', time() - tic)    
    
    if output:
        tic = time()
        self.output_report()
        self.dump_time('output_report', time() - tic)   
    
    # Mesh Network
    tic = time()
    self.mesh_network()
    self.dump_time('Function: mesh_network', time() - tic)  
    print ('='*80)
    print 'dfnGen Complete'
    print ('='*80)
    print ''
    self.dump_time('Process: dfnGen',time() - tic_gen)  

def make_working_directory(self):
    ''' Make working directory for dfnWorks Simulation

    Parameters
    ----------
    DFN Class

    Returns
    -------
    None

    Notes
    -----
    If directory already exists, user is prompted if they want to overwrite and proceed. If not, program exits. 
    '''    

    try:
        os.mkdir(self.jobname)
    except OSError:
        print '\nFolder ', self.jobname, ' exists'
        keep = raw_input('Do you want to delete it? [yes/no] \n')
        if keep == 'yes' or keep == 'y':
            print 'Deleting', self.jobname 
            shutil.rmtree(self.jobname)
            print 'Creating', self.jobname 
            os.mkdir(self.jobname)    
        elif keep == 'no' or 'n':
            sys.exit("Not deleting folder. Exiting Program") 
        else:
            sys.exit("Unknown Response. Exiting Program") 
    os.mkdir(self.jobname + '/radii')
    os.mkdir(self.jobname + '/intersections')
    os.mkdir(self.jobname + '/polys')
    os.chdir(self.jobname)
    
    print("Current directory is now: %s\n"%os.getcwd())
    print("Jobname is %s"%self.jobname) 

def create_network(self):
    ''' Execute dfnGen

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    After generation is complete, this script checks whether the generation of the fracture network failed or succeeded based on the existance of the file params.txt. 
    '''
    print('--> Running DFNGEN') 
    # copy input file into job folder    
    cmd = os.environ['DFNGEN_EXE']+' '+ self.local_dfnGen_file[:-4] + '_clean.dat' + ' ' + self.jobname
    print("Running %s"%cmd)
    subprocess.call(cmd, shell = True) 

    if os.path.isfile("params.txt") is False:
        sys.exit("ERROR! Generation Failed\nExiting Program.")
    else:
        print('-'*80)
        print("Generation Succeeded")
        print('-'*80)
