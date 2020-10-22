#!/bin/bash
#SBATCH -n 4
#SBATCH --ntasks-per-node=4
#SBATCH -p nanopetro-intel
 
module purge
 
# calling the qe-module on josephson
 
# Intel nodes 
 
module load quantum-espresso-6.4.1-gcc-8.3.0-grab7h5
  
  
srun generate_vdW_kernel_table.x
 
 
srun -K -n 4 pw.x  <confr2.in >  co.out
