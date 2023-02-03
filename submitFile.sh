# Export current environment
#$ -V
# Set a 10 min limit
#$ -l h_rt=48:00:00
#$ -m be
#$ -pe smp 18
# Load matlab module
module add user
module load matlab/R2021b
module load anaconda
module add abaqus
export LM_LICENSE_FILE=27004@abaqus-server1.leeds.ac.uk:$LM_LICENSE_FILE
export ABAQUSLM_LICENSE_FILE=$LM_LICENSE_FILE
# run matlab using command file
# -nodisplay flag should be given to suppress graphics
unset GOMP_CPU_AFFINITY KMP_AFFINITY
matlab -nodisplay < runFile.m