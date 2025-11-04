#!/bin/bash -l
echo =========================================================   
echo Job submitted  date = Fri 26 Sep 09:36:06 BST 2025      
date_start=`date +%s`
echo $SLURM_JOB_NUM_NODES nodes \( $SLURM_CPUS_ON_NODE processes per node \)        
echo $SLURM_JOB_NUM_NODES hosts used: $SLURM_JOB_NODELIST      
# Set this otherwise a different transport gets selected on some nodes and things break in strange ways
export OMPI_MCA_pml=^cm
echo Job output begins                                           
echo -----------------                                           
echo   
#hostname

# Need to set the max locked memory very high otherwise IB can't allocate enough and fails with "UCX  ERROR Failed to allocate memory pool chunk: Input/output error"
ulimit -l unlimited

export OMP_NUM_THEADS=1
 /usr/local/shared/slurm/bin/srun -u -n 1 --mpi=pmix --mem-per-cpu=81920 nice -n 10 /mnt/zfsusers/hollowayp/paltas/./generate_images_sequentially.sh _mu3_B_theta_E_-1pct
  echo ---------------                                           
  echo Job output ends                                           

  date_end=`date +%s`
  seconds=$((date_end-date_start))
  minutes=$((seconds/60))
  seconds=$((seconds-60*minutes))
  hours=$((minutes/60))
  minutes=$((minutes-60*hours))
  echo =========================================================   
  echo PBS job: finished   date = `date`   
  echo Total run time : $hours Hours $minutes Minutes $seconds Seconds
  echo =========================================================
