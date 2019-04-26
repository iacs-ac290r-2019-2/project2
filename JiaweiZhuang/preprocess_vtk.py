import numpy as np
import xarray as xr
from numba import jit
import glob

import vtki

@jit(nopython=True)
def _assign_values(dr_data, coord_idx, target_data, n_points):
    '''
    Fill structed 3d array from unstructued 1d data.

    Input
    -----
    dr_data: 3d numpy array, to be modified in-place
    
    coord_idx: 2d numpy array of shape (n_points, 3), coordinate indice for 1d array
    
    target_data: 1d numpy array of shape (n_points, 3), the 1d array to map
    
    n_points: int, total number of data points (i.e. target_data.size)
    '''
    for i in range(n_points):
        ix=coord_idx[i, 0]
        iy=coord_idx[i, 1]
        iz=coord_idx[i, 2]
        dr_data[ix, iy, iz] = target_data[i]


def vtk_to_xarray(filename, scalar_names=[], vector_names=[], point_to_center=False):
    '''
    Convert unstructued VTK file to structued xarray Dataset.

    Input
    -----
    filename: str, VTK file, '*.vtu' or '*.pvtu'

    scalar_names: list of str, scalar variable names in VTK file, e.g. 'density', 'temperature'

    vector_names: list of str, vector variable names in VTK file, e.g. 'velocity'

    point_to_center: bool, whether to convert cell data to point data
    
    Return
    ------
    ds: xarray DataSet
    '''
    # Note: do not modify scalar_names and vector_names in-place, as that would permanently change default arguments

    data_vtk = vtki.read(filename)
    
    if point_to_center:
        data_vtk = data_vtk.cell_centers()

    # coordinate values in original VTK file (unstructed, 1d)
    coord = np.asarray(data_vtk.points)
    icoord = coord.astype(int)
    n_points = icoord.shape[0]

    # coordinate values for each dimension
    x_1d = np.unique(icoord[:,0])
    y_1d = np.unique(icoord[:,1])
    z_1d = np.unique(icoord[:,2])

     # move offset to zero, for array indexing
    coord_idx = icoord - np.array([x_1d.min(), y_1d.min(), z_1d.min()]) 


    dr_list = []

    for varname in scalar_names:

        # placeholder for 3d structed multi-dimensional data
        # use float32 to match original VTK file
        dr_data = np.empty((x_1d.size, y_1d.size, z_1d.size), dtype=np.float32)
        dr_data.fill(np.nan)

        target_data = data_vtk.point_arrays[varname]
        assert np.equal(n_points, target_data.size)  # sanity check

        # 1d -> 3d mapping
        _assign_values(dr_data, coord_idx, target_data, n_points)

        # add coordinate metadata
        dr_temp = xr.DataArray(dr_data, name=varname, 
                               dims=('x', 'y', 'z'), coords={'x': x_1d, 'y': y_1d, 'z': z_1d})

        dr_list.append(dr_temp)

    for varname in vector_names:

        target_data = data_vtk.point_arrays[varname]
        assert np.equal(n_points, target_data.shape[0])  # sanity check
        assert target_data.shape[1] == 3

        component_names = [varname + suffix for suffix in ['_x', '_y', '_z']]

        for idim in [0, 1, 2]:
            # placeholder for 3d structed multi-dimensional data
            dr_data = np.empty((x_1d.size, y_1d.size, z_1d.size), dtype=np.float32)
            dr_data.fill(np.nan)

            # 1d -> 3d mapping
            _assign_values(dr_data, coord_idx, target_data[:,idim], n_points)

            # add coordinate metadata
            dr_temp = xr.DataArray(dr_data, name=component_names[idim], 
                                dims=('x', 'y', 'z'), coords={'x': x_1d, 'y': y_1d, 'z': z_1d})

            dr_list.append(dr_temp)

    ds = xr.merge(dr_list)
    
    return ds


def multistep_vtk_to_netcdf(filelist_bld, filelist_drug, outdir_bld, outdir_drug):
    '''
    Convert multiple Murphy VTK files to netcdf format
    Unstructured meshes are re-organized to structured multi-dimensional grids, for easy computation.
    The data size is also 10x smaller due to more efficient data format.
    
    Remember to clean duplicate files before running this function, otherwise will have permission error.
    
    Input
    -----
    filelist_bld: list of strings, Murphy output blood field, '*.pvtu'
    
    filelist_drug: list of strings, Murphy output drug field, '*.pvtu'
    
    outdir_bld: string, output directory for blood field
    On Odyssey it is like
    '/n/scratchlfs/ac290r/p2_data_postprocess/re10_pe1/blood/'
    
    outdir_drug: string, output directory for drug field
    On Odyssey it is like
    '/n/scratchlfs/ac290r/p2_data_postprocess/re10_pe1/drug/'
    
    Return
    ------
    None, write files to disk
    
    '''
    
    # time stamp truncation
    # e.g. 'xxx/VTK/T0004000000.pvtu' -> '04000000'
    s_start, s_end = (-13, -5)
    
    for filename in filelist_bld:
        time_stamp = filename[s_start:s_end]
        print('processing', time_stamp)
        
        print('opening file:', filename)
        ds_temp = vtk_to_xarray(filename, scalar_names=['density'], vector_names=['velocity'])

        nc_filename = outdir_bld + 'blood_' + time_stamp + '.nc'
        print('writing to file:', nc_filename)
        ds_temp.to_netcdf(nc_filename)
        
    for filename in filelist_drug:
        time_stamp = filename[s_start:s_end]
        print('processing', time_stamp)
        
        print('opening file:', filename)
        dr_temp = vtk_to_xarray(filename, scalar_names=['density'])['density']
        
        nc_filename = outdir_drug + 'drug_' + time_stamp + '.nc'
        print('writing to file:', nc_filename)
        dr_temp.to_netcdf(nc_filename)
        
        
def sglob(pathname):
    '''Sorted glob'''
    return sorted(glob.glob(pathname))

    
if __name__ == '__main__':

    # == Input arguments ==
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--thin", type=int, default=40,
                        help="downsample rate")
    parser.add_argument("--case", type=str, default=None,
                        help="choose from 're5pe1', 're5pe3', 're10pe1', 're10pe3'")
    args = parser.parse_args()

    print("Arguments:", args)
    
    # == Global constants ==
    
    # Input files
    filelists_bld = {}
    filelists_bld['re5pe1'] = sglob('/n/scratchlfs/ac290r/p2_re5_pe1/DIRDATA_Blood/VTK/*.pvtu')
    filelists_bld['re5pe3'] = sglob('/n/scratchlfs/ac290r/p2_re5_pe3/DIRDATA_Blood/VTK/*.pvtu')
    filelists_bld['re10pe1'] = sglob('/n/scratchlfs/ac290r/p2_re10_pe1/DIRDATA_Blood/VTK/*.pvtu')
    filelists_bld['re10pe3'] = sglob('/n/scratchlfs/ac290r/p2_re10_pe3/DIRDATA_Blood/VTK/*.pvtu')
    
    filelists_drug = {}
    filelists_drug['re5pe1'] = sglob('/n/scratchlfs/ac290r/p2_re5_pe1/DIRDATA_Drug/VTK/*.pvtu')
    filelists_drug['re5pe3'] = sglob('/n/scratchlfs/ac290r/p2_re5_pe3/DIRDATA_Drug/VTK/*.pvtu')
    filelists_drug['re10pe1'] = sglob('/n/scratchlfs/ac290r/p2_re10_pe1/DIRDATA_Drug/VTK/*.pvtu')
    filelists_drug['re10pe3'] = sglob('/n/scratchlfs/ac290r/p2_re10_pe3/DIRDATA_Drug/VTK/*.pvtu')
    
    # Equivalent:
    # for case in ['re5pe1', 're5pe10', 're10pe1', 're10pe10']:
    #     filelists_bld[case] = sglob('/n/scratchlfs/ac290r/p2_' + case + '/DIRDATA_Blood/VTK/*.pvtu')
    #     filelists_drug[case] = sglob('/n/scratchlfs/ac290r/p2_' + case + '/DIRDATA_Drug/VTK/*.pvtu')
    # Do not use for loop so we can easily change to special runs
    
    print('number of raw files:')
    print([len(filelist) for filelist in filelists_bld.values()])
    print([len(filelist) for filelist in filelists_drug.values()])
    
    # Output files
    TOPDIR = '/n/scratchlfs/ac290r/p2_data_postprocess/'
    dest_dir = {}
    
    dest_dir['re5pe1'] = (TOPDIR+'re5_pe1/blood/', TOPDIR+'re5_pe1/drug/')
    dest_dir['re5pe3'] = (TOPDIR+'re5_pe3/blood/', TOPDIR+'re5_pe3/drug/')
    dest_dir['re10pe1'] = (TOPDIR+'re10_pe1/blood/', TOPDIR+'re10_pe1/drug/')
    dest_dir['re10pe3'] = (TOPDIR+'re10_pe3/blood/', TOPDIR+'re10_pe3/drug/')
    
    # Equivalent:
    # for case in ['re5pe1', 're5pe10', 're10pe1', 're10pe10']:
    #     dest_dir[case] = (TOPDIR + case + 'blood/', TOPDIR + case + 'drug/')
    
    
    # == Start processing ==
    case = args.case
    thin = args.thin
    
    if case is None:  # dry run
        pass
    
    elif case in ['re5pe1', 're5pe3', 're10pe1', 're10pe3']:
        multistep_vtk_to_netcdf(filelists_bld[case][::thin], filelists_drug[case][::thin], dest_dir[case][0], dest_dir[case][1])
        
    else:
        raise ValueError('Undefined case name')