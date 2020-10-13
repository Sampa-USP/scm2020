#!/bin/bash
#SBATCH -n 14 
#SBATCH --ntasks-per-node=14
#SBATCH -p nanopetro-intel

mpirun -n 2 pw.x < 01.in > 01.out


