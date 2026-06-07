#!/bin/bash
#SBATCH --time=96:00:00
#SBATCH --account=def-kleinke
#SBATCH --mem=256G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=BaLaCuSe3_dos
#SBATCH --mail-type=ALL
#SBATCH --mail-user=royhe62@yahoo.ca
#SBATCH --output=BaLaCuSe3_dos-output.txt
#SBATCH --error=BaLaCuSe3_dos-errors.txt

module purge

module load StdEnv/2023  # Loads the default software environment
module load gcc/12.3
module load openmpi/4.1.5
module load gromacs/2025.4
module load apptainer/1.2.4
module load cuda/12.6
echo "Hello!"


i=1
while IFS= read -r config_name; do
  apptainer exec   /home/royhe62/scratch/sifs/hcnn.sif python code/classification/train.py -c "classification/config/${config_name}" \
    > "outputs/exp_${i}.txt" 2>&1

  i=$((i + 1))
done < config_list.txt
