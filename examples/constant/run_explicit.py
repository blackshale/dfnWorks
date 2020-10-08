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

DFN.make_working_directory(delete=True)

## dfnGen
DFN.check_input()
DFN.create_network()
#DFN.output_report()
DFN.mesh_network(visual_mode=True,production_mode=False)

DFN.set_flow_solver("PFLOTRAN")
DFN.inp_file = "octree_dfn.inp"

DFN.map_to_continuum(l=0.25,orl=3)
DFN.upscale(mat_perm=1e-15,mat_por=0.01)
exit()

##dfnFlow()
DFN.lagrit2pflotran()
DFN.pflotran()
DFN.parse_pflotran_vtk_python()       
DFN.pflotran_cleanup()

# dfnTrans
DFN.copy_dfn_trans_files()
DFN.check_dfn_trans_run_files()
DFN.run_dfn_trans()

main_elapsed = time() - main_time
timing = 'Time Required: %0.2f Minutes'%(main_elapsed/60.0)
print("*"*80)
print(DFN.jobname+' complete')
print("Thank you for using dfnWorks")
print("*"*80)
