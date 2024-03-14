#!/bin/bash

#======================================================
#
# Job script for running DAMASK on multiple cores (shared)
#
#======================================================

#======================================================
# Propogate environment variables to the compute node
#SBATCH --export=ALL
#
# Run in the standard partition (queue)
#SBATCH --partition=standard
#
# Specify project account
#SBATCH --account=rahimi-omp
#
# No. of tasks required
#SBATCH --cpus-per-task=2
#
# Specify (hard) runtime (HH:MM:SS)
#SBATCH --time=00:20:00
#
# Job name
#SBATCH --job-name=damask_test
#
# Output file
#SBATCH --output=slurm-%j.out
#======================================================


unset SLURM_GTIDS

#======================================================
# Prologue script to record job details
# Do not change the line below
#======================================================
/opt/software/scripts/job_prologue.sh 
#------------------------------------------------------

. ../src/conda_initialise-3.9.sh

conda activate env_for_damask_LR

export OPENBLAS_NUM_THREADS=1

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

DAMASK_grid --load ../input/loadZ.yaml --geom ../input/cubes_n4-8-cells-per-side.vti

#======================================================
# Epilogue script to record job endtime and runtime
# Do not change the line below
#======================================================
/opt/software/scripts/job_epilogue.sh
#------------------------------------------------------
