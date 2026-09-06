#!/bin/bash
#SBATCH --job-name=feelpp-heat
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:15:00
#SBATCH --output=feelpp-%j.out
#SBATCH --error=feelpp-%j.err
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
# Add site-approved module setup above this check if needed.
command -v apptainer
sha256sum -c feelpp.sif.sha256
sha256sum -c case.sha256
run_dir="$PWD/results/$SLURM_JOB_ID"
mkdir -p "$run_dir"
apptainer --version
srun --mpi=none apptainer exec --cleanenv "$PWD/feelpp.sif" \
    feelpp_toolbox_heat --version
srun --mpi=none apptainer exec --cleanenv \
    --bind "$PWD/case:/case:ro,$run_dir:/results:rw" \
    --env OMP_NUM_THREADS=1 \
    "$PWD/feelpp.sif" feelpp_toolbox_heat \
    --config-file /case/case2.cfg --directory /results
