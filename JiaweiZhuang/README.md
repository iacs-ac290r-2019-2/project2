# Murphy post-processing scripts

This directory mostly contains post-processing scripts for Module 2 Murphy output.

## Python Environment setup

    conda env create -n vtk_env -f ./vtk_environment.yml

The steps to run Jupyter on Odyssey is the same as in Module 1:
- https://github.com/JiaweiZhuang/process_drekar_output

To read files on Odyssey `/n/scratchlfs/`, definitely run Python/Jupyter on compute nodes. The connection from login-node to scratchlfs is extremely slow (at least 10x slower).

## Convert Murphy unstructured VTK output to gridded, compressed NetCDF

- Python script: [preprocess_vtk.py](./preprocess_vtk.py)

- Slurm script to run the Python script: [submit_preprocess.sh](./submit_preprocess.sh)

This make the output data 10x smaller (for each time step), and even 50x smaller with 5x downsamping (the `thin` parameter in script). The NetCDF data are gridded, structured 3D arrays, so are much easier to analyze. Data on undefined mesh points are set as `nan`.

## Data visualization and computation


