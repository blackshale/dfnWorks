"""
.. file:: run_dfnworks.py
   :synopsis: run file for dfnworks 
   :version: 1.0
   :maintainer: Jeffrey Hyman, Carl Gable, Nathaniel Knapp
.. moduleauthor:: Jeffrey Hyman <jhyman@lanl.gov>

"""

import os, sys
from time import time
from pydfnworks import * 
import subprocess

define_paths()
main_time = time()
DFN = create_dfn()

DFN.make_working_directory()
DFN.check_input()
DFN.create_network()

#DFN.output_report()
DFN.set_flow_solver("PFLOTRAN")
DFN.mesh_network(uniform_mesh=True)

restart_file = "DUMMY/dfnworks-main/examples/ade_example/dfn_restart.in"
DFN.lagrit2pflotran()
DFN.pflotran(restart=True,restart_file=restart_file)

DFN.parse_pflotran_vtk_python()       
DFN.pflotran_cleanup()
DFN.pflotran_cleanup(index_finish=100,filename=restart_file)


main_elapsed = time() - main_time
timing = 'Time Required: %0.2f Minutes'%(main_elapsed/60.0)
print("*"*80)
print(DFN.jobname+' complete')
print("Thank you for using dfnWorks")
print("*"*80)

