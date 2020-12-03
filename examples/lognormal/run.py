#"""
#   :synopsis: run file for dfnworks 
#   :version: 1.0
#   :maintainer: Jeffrey Hyman
#.. moduleauthor:: Jeffrey Hyman <jhyman@lanl.gov>
#"""

import os, sys
from time import time
from pydfnworks import * 


define_paths()
main_time = time()
DFN = create_dfn()
# General Work Flow
DFN.dfn_gen()
DFN.dfn_flow()
DFN.dfn_trans()

main_elapsed = time() - main_time
DFN.dump_time("Total Time: ",main_elapsed) 
DFN.print_run_time()	
print("*"*80)
print(DFN.jobname+' complete')
print("Thank you for using dfnWorks")
print("*"*80)

