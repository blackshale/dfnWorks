"""
.. module:: mesh_dfn.py
   :synopsis: meshing driver for DFN 
.. moduleauthor:: Jeffrey Hyman <jhyman@lanl.gov>

"""

import os
import sys
from time import time
from numpy import genfromtxt, sort
# pydfnworks Modules
from pydfnworks.dfnGen import mesh_dfn_helper as mh
from pydfnworks.dfnGen import lagrit_scripts as lagrit
from pydfnworks.dfnGen import run_meshing as run_mesh


def mesh_network(self,
                 prune=False,
                 uniform_mesh=False,
                 production_mode=True,
                 refine_factor=1,
                 slope=2,
                 visual_mode=None):
    ''' Mesh fracture network using LaGriT

    Parameters
    ----------
        self : object 
            DFN Class
        prune : bool
            If prune is False, mesh entire network. If prune is True, mesh only fractures in self.prune_file 
        uniform_mesh : bool
            If true, mesh is uniform resolution. If False, mesh is spatially variable            
        production_mode : bool
            If True, all working files while meshing are cleaned up. If False, then working files will not be deleted
        refine_factor : float
            Determines distance for mesh refinement (default=1)
        slope : float 
            Slope of piecewise linear function determining rate of coarsening. 
        visual_mode : None
            If the user wants to run in a different meshing mode from what is in params.txt, set visual_mode = True/False on command line to override meshing mode

    Returns
    -------
        None

    Notes
    ------
    1. For uniform resolution mesh, set slope = 0
    2. All fractures in self.prune_file must intersect at least 1 other fracture

    '''
    print('=' * 80)
    print("Meshing Network Using LaGriT : Starting")
    print('=' * 80)

    if uniform_mesh:
        slope = 0  # Setting slope = 0, results in a uniform mesh

    if prune:
        if self.prune_file == "":
            error = "ERROR!! User requested pruning in meshing but \
did not provide file of fractures to keep.\nExiting program.\n"

            sys.stderr.write(error)
            sys.exit(1)

        mh.create_mesh_links(self.path)
        num_poly, h, params_visual_mode, dudded_points, domain = mh.parse_params_file(
        )
        if visual_mode == None:
            visual_mode = params_visual_mode

        print("Loading list of fractures to remain in network from %s" %
              self.prune_file)
        fracture_list = sort(genfromtxt(self.prune_file).astype(int))
        print(fracture_list)
        if not visual_mode:
            lagrit.edit_intersection_files(num_poly, fracture_list, self.path)
        num_poly = len(fracture_list)

    else:
        num_poly, h, params_visual_mode, dudded_points, domain = mh.parse_params_file(
        )
        if visual_mode == None:
            visual_mode = params_visual_mode
        fracture_list = range(1, num_poly + 1)

    # if number of fractures is greater than number of CPUS,
    # only use num_poly CPUs. This change is only made here, so ncpus
    # is still used in PFLOTRAN
    ncpu = min(self.ncpu, num_poly)
    lagrit.create_parameter_mlgi_file(fracture_list, h, slope=slope)
    lagrit.create_lagrit_scripts(visual_mode, ncpu)
    lagrit.create_user_functions()
    failure = run_mesh.mesh_fractures_header(fracture_list, ncpu, visual_mode)
    if failure:
        mh.cleanup_dir()
        error = "One or more fractures failed to mesh properly.\nExiting Program\n"
        sys.stderr.write(error)
        sys.exit(1)

    n_jobs = lagrit.create_merge_poly_files(ncpu, num_poly, fracture_list, h,
                                            visual_mode, domain,
                                            self.flow_solver)
    run_mesh.merge_the_meshes(num_poly, ncpu, n_jobs, visual_mode)

    if (not visual_mode and not prune):
        if not mh.check_dudded_points(dudded_points):
            mh.cleanup_dir()
            error = "ERROR!!! Incorrect Number of dudded points.\nExiting Program\n"
            sys.stderr.write(error)
            sys.exit(1)

    if production_mode:
        mh.cleanup_dir()

    if not visual_mode:
        lagrit.define_zones()

    if prune:
        mh.clean_up_files_after_prune(self)

    mh.output_meshing_report(self.local_jobname, visual_mode)
    print("--> Meshing Complete")
