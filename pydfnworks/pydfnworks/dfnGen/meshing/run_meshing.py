"""
.. module:: run_meshing.py
   :synopsis: functions to mesh fracture network in parallel 
.. moduleauthor:: Jeffrey Hyman <jhyman@lanl.gov>

"""

import subprocess
import os
import sys
import timeit
import glob

import multiprocessing as mp
from shutil import copy, rmtree
from numpy import genfromtxt
from pydfnworks.dfnGen.meshing import mesh_dfn_helper as mh
from pydfnworks.dfnGen.meshing.poisson_disc.poisson_functions import single_fracture_poisson


def cleanup_failed_run(fracture_id, digits, quite=True):
    """ If meshing fails, this function moves all relavent files
    to a folder for debugging

    Parameters
    ----------
        fracture_id : int
            Current Fracture ID number
        digits : int
            Number of digits in total number of fractures

    Returns
    -------
        None

    Notes
    ------
    This will throw warnings depending on when in the work-flow it is called. Some files
    might not be created at those times. It's okay.

"""

    if not quite:
        print(f"--> Cleaning up meshing run for fracture {fracture_id}")

    if not os.path.isfile("failure.txt"):
        with open('failure.txt', "w+") as failure_file:
            failure_file.write(f"{fracture_id}\n")
    else:
        with open('failure.txt', "a") as failure_file:
            failure_file.write(f"{fracture_id}\n")

    folder = f"failure_{fracture_id}/"
    try:
        os.mkdir(folder)
    except:
        if not quite:
            print(f"Warning! Unable to make new folder: {folder}")
        pass

    files = [
        f"mesh_{fracture_id}.inp", f"{fracture_id}_mesh_errors.txt",
        f"id_tri_node_{fracture_id}.list",
        f"lagrit_logs/log_lagrit_{fracture_id:0{digits}d}.out"
    ]

    for f in files:
        try:
            copy(f, folder)
        except:
            if not quite:
                print(f'--> Warning: Could copy {f} to failure folder')
            pass

    symlinks = [
        f"poly_{fracture_id}.inp", f"intersections_{fracture_id}.inp",
        f"parameters_{fracture_id}.mlgi", f"mesh_poly_{fracture_id}.lgi",
        f'points_{fracture_id}.xyz'
    ]

    for f in symlinks:
        try:
            os.unlink(f)
        except:
            if not quite:
                print(f'--> Warning: Could not unlink {f}')
            pass

    if not quite:
        print(f"--> Cleanup for Fracture {fracture_id} complete")


def mesh_fracture(fracture_id, visual_mode, num_poly):
    """Child function for parallelized meshing of fractures

    Parameters
    ----------
        fracture_id : int
            Current Fracture ID number
        visual_mode : bool
            True/False for reduced meshing
        num_poly : int 
            Total Number of Fractures in the DFN

    Returns
    -------
        success index: 
        0 - run was successful
        -1 - error making symbolic link
        -2 - run failed in Poisson Sampling
        -3 - run failed to produce mesh files
        -4 - line of intersection not preserved
    
    Notes
    -----
    If meshing run fails, information about that fracture will be put into a directory failure_(fracture_id)

    """

    # get current process information
    p = mp.current_process()
    _, cpu_id = p.name.split("-")
    cpu_id = int(cpu_id)
    # get leading digits
    digits = len(str(num_poly))

    print(
        f"--> Fracture {fracture_id:0{digits}d} out of {num_poly} is starting on worker {cpu_id}"
    )

    tic = timeit.default_timer()
    # Create Symbolic Links
    try:
        os.symlink(f"polys/poly_{fracture_id}.inp", f"poly_{fracture_id}.inp")
    except:
        print(f"-->\n\n\nError creating link for poly_{fracture_id}.inp\n\n\n")
        return (fracture_id, -1)

    try:
        os.symlink(f"parameters/parameters_{fracture_id}.mlgi",\
            f"parameters_{fracture_id}.mlgi")
    except:
        print(
            f"-->\n\n\nError creating link for/parameters_{fracture_id}.mlgi\n\n\n"
        )
        return (fracture_id, -1)

    try:
        os.symlink(f"lagrit_scripts/mesh_poly_{fracture_id}.lgi",\
            f"mesh_poly_{fracture_id}.lgi")
    except:
        print(
            f"-->\n\n\nError creating link for/parameters_{fracture_id}.mlgi\n\n\n"
        )
        return (fracture_id, -1)

    if not visual_mode:
        try:
            os.symlink(f"intersections/intersections_{fracture_id}.inp",\
                f"intersections_{fracture_id}.inp")
        except:
            print(
                f"\n\n\n--> Error creating link for intersections_{fracture_id}.inp\n\n\n"
            )
            return (fracture_id, -1)

        ## Poisson Disc Sampling Code Here ##
        try:
            single_fracture_poisson(fracture_id)
        except:
            print(" Error:", sys.exc_info()[0])
            print(
                f"-->\n\n\nERROR occurred generating points for fracture {fracture_id}\n\n\n"
            )
            cleanup_failed_run(fracture_id, digits)
            return (fracture_id, -2)
        ## Poisson Disc Sampling Code Here ##

        # check if points were created, if not exit
        if not os.path.isfile(f'points/points_{fracture_id}.xyz'):
            print(
                f"-->\n\n\nERROR occurred generating points for fracture {fracture_id}\n\n\n"
            )
            cleanup_failed_run(fracture_id, digits)
            return (fracture_id, -2)
        try:
            os.symlink(f"points/points_{fracture_id}.xyz",
                       f"points_{fracture_id}.xyz")
        except:
            print(
                f"-->\n\n\nError creating link for points_{fracture_id}.xyz\n\n\n"
            )
            return (fracture_id, -1)

    # run LaGriT Meshing
    try:
        mh.run_lagrit_script(
            f"mesh_poly_{fracture_id}.lgi",
            output_file=f"lagrit_logs/log_lagrit_{fracture_id:0{digits}d}.out",
            quite=True)
    except:
        print(
            f"\n\n\n--> ERROR occurred during meshing fracture {fracture_id}\n\n\n"
        )
        cleanup_failed_run(fracture_id, digits)
        return (fracture_id, -3)

    # Check if mesh*.lg file was created, if not exit.
    if not os.path.isfile(f'mesh_{fracture_id}.lg') or os.stat(
            f'mesh_{fracture_id}.lg') == 0:
        print(
            f"\n\n\n--> ERROR occurred during meshing fracture {fracture_id}\n\n\n"
        )
        cleanup_failed_run(fracture_id, digits)
        return (fracture_id, -3)

    ## Once meshing is complete, check if the lines of intersection are in the final mesh
    if not visual_mode:

        cmd_check = f"{os.environ['CONNECT_TEST_EXE']} \
            intersections_{fracture_id}.inp \
            id_tri_node_{fracture_id}.list \
            mesh_{fracture_id}.inp \
            {fracture_id}"

        # If the lines of intersection are not in the final mesh, put depending files
        # into a directory for debugging.
        try:
            if subprocess.call(cmd_check, shell=True):
                print(
                    f"\n\n\n--> ERROR: MESH CHECKING FAILED on {fracture_id}!!!\n\nEXITING PROGRAM\n\n\n"
                )
                cleanup_failed_run(fracture_id, digits)
                return (fracture_id, -4)
        except:
            print(
                f"\n\n\n--> ERROR: MESH CHECKING FAILED on {fracture_id}!!!\n\nEXITING PROGRAM\n\n\n"
            )
            cleanup_failed_run(fracture_id, digits)
            return (fracture_id, -4)

        # Mesh checking was a success. Remove check files and move on
        files = [f"id_tri_node_{fracture_id}.list", f"mesh_{fracture_id}.inp"]
        for f in files:
            try:
                os.remove(f)
            except:
                print(f"--> Could not remove {f}\n")
                pass

    # Remove symbolic
    if visual_mode:
        files = [
            f'poly_{fracture_id}.inp', f'parameters_{fracture_id}.mlgi',
            f"mesh_poly_{fracture_id}.lgi"
        ]
    else:
        files = [
            f'poly_{fracture_id}.inp', f'intersections_{fracture_id}.inp',
            f'points_{fracture_id}.xyz', f'parameters_{fracture_id}.mlgi',
            f"mesh_poly_{fracture_id}.lgi"
        ]
    for f in files:
        try:
            os.unlink(f)
        except:
            print(f'--> Warning: Could unlink {f}')
            pass

    elapsed = timeit.default_timer() - tic
    print(
        f"--> Fracture {fracture_id:0{digits}d} out of {num_poly} is complete on worker {cpu_id}. Time required: {elapsed:.2f} seconds\n"
    )
    return (fracture_id, 0)


def mesh_fractures_header(fracture_list, ncpu, visual_mode, h):
    """ Header function for Parallel meshing of fractures
    
    Creates a queue of fracture numbers ranging from 1, num_poly
    
    Each fractures is meshed using mesh_fracture called within the
    worker function.

    If any fracture fails to mesh properly, then a folder is created with 
    that fracture information and the fracture number is written into
    failure.txt.

    Parameters
    ----------
        fracture_list : list
            Fractures to be meshed
        visual_mode : bool
            True/False for reduced meshing
        num_poly : int
            Total Number of Fractures

    Returns
    -------
        True/False : bool
            True - If failure.txt is empty then all fractures have been meshed correctly
            False - If failure.txt is not empty, then at least one fracture failed.  

    Notes
    -----
        If one fracture fails meshing, program will exit. 

    """
    t_all = timeit.default_timer()
    print()
    print('=' * 80)
    print(
        f"\n--> Triangulating {len(fracture_list)} fractures using {ncpu} processors\n\n"
    )
    dirs = ["points", "lagrit_logs"]
    for d in dirs:
        if os.path.isdir(d):
            rmtree(d)
            os.mkdir(d)
        else:
            os.mkdir(d)

    pool = mp.Pool(ncpu)
    result_list = []

    def log_result(result):
        # This is called whenever foo_pool(i) returns a result.
        # result_list is modified only by the main process, not the pool workers.
        result_list.append(result)
        if result[1] != 0:
            pool.terminate()
            # If a run fails, kill all other processes, and clean up the directory
            names = [
                "poly_*.inp", "mesh_poly_*.lgi", "parameters_*.mlgi",
                "intersections_*.inp", "points_*.xzy"
            ]
            for name in names:
                files_to_remove = glob.glob(name)
                for f in files_to_remove:
                    os.remove(f)

    for i in fracture_list:
        pool.apply_async(mesh_fracture,
                         args=(i, visual_mode, len(fracture_list)),
                         callback=log_result)

    pool.close()
    pool.join()

    for result in result_list:
        if result[1] != 0:
            print(
                f"\n\n--> Fracture number {result[0]} failed with error {result[1]}\n"
            )
            details = """
Error Index:
-1 - error making symbolic link
-2 - run failed in Poisson Sampling
-3 - run failed to produce mesh files
-4 - line of intersection not preserved
        """
            print(details)
            return 1

    elapsed = timeit.default_timer() - t_all

    if os.path.isfile("failure.txt"):
        failure_list = genfromtxt("failure.txt")
        failure_flag = True
        if type(failure_list) is list:
            failure_list = sort(failure_list)
        else:
            print('--> Fractures:', failure_list, 'Failed')
        print('--> Main process exiting.')
    else:
        failure_flag = False

        print('--> Triangulating Polygons: Complete')
        time_sec = elapsed
        time_min = elapsed / 60
        time_hrs = elapsed / 3600

        print("--> Total Time to Mesh Network:")
        print(
            f"--> {time_sec:.2e} seconds\t{time_min:.2e} minutes\t{time_hrs:.2e} hours"
        )

        print('=' * 80)
    return failure_flag


def merge_worker(job):
    """Parallel worker for merge meshes into final mesh 

    Parameters
    ----------
        job : int
            job number

    Returns
    -------
        bool : True if failed / False if successful

    Notes
    -----
    """

    print(f"--> Starting merge: {job}")
    tic = timeit.default_timer()

    if mh.run_lagrit_script(f"lagrit_scripts/merge_poly_part_{job}.lgi",
                            f"lagrit_logs/log_merge_poly_part{job}.out",
                            quite=True):
        print(f"Error {job} failed")
        return True

    elapsed = timeit.default_timer() - tic
    print(
        f"--> Merge Number {job} Complete. Time elapsed: {elapsed:.2f} seconds."
    )
    return False


def merge_the_meshes(num_poly, ncpu, n_jobs, visual_mode):
    """Runs the LaGrit Scripts to merge meshes into final mesh 

    Parameters
    ----------
        num_poly : int
            Number of Fractures
        ncpu : int
            Number of Processors
        n_jobs : int
            Number of mesh pieces
        visual_mode : bool
            True/False for reduced meshing

    Returns
    -------
        None

    Notes
    -----
        Meshes are merged in batches for efficiency  
    """
    print('=' * 80)
    if n_jobs == 1:
        print(
            f"--> Merging triangulated fracture meshes using {n_jobs} processor."
        )
    else:
        print(
            f"--> Merging triangulated fracture meshes using {n_jobs} processors."
        )

    jobs = range(1, n_jobs + 1)
    tic = timeit.default_timer()
    num_cpu = len(jobs)
    pool = mp.Pool(num_cpu)
    outputs = pool.map(merge_worker, jobs)
    pool.close()
    pool.join()
    pool.terminate()
    elapsed = timeit.default_timer() - tic
    print(
        f"\n--> Initial merging complete. Time elapsed: {elapsed:.2f} seconds.\n"
    )
    for output in outputs:
        if output:
            error = "ERROR!!! One of the merges failed\nExiting\n"
            sys.stderr.write(error)
            sys.exit(1)

    print('=' * 80)
    print("--> Starting Final Merge")
    tic = timeit.default_timer()

    mh.run_lagrit_script('lagrit_scripts/merge_rmpts.lgi',
                         'lagrit_logs/log_merge_all.out',
                         quite=True)

    elapsed = timeit.default_timer() - tic
    print(f"--> Final merge took {elapsed:.2f} seconds")

    if not visual_mode:
        if (os.stat("full_mesh.lg").st_size > 0):
            print("--> Final merge successful")

        else:
            error = "ERROR: Final merge Failed\n"
            sys.stderr.write(error)
            sys.exit(1)

    else:
        if os.stat("reduced_mesh.inp").st_size > 0:
            print("--> Final merge successful")
        else:
            error = "ERROR: Final merge Failed\n"
            sys.stderr.write(error)
            sys.exit(1)
    print('=' * 80)
