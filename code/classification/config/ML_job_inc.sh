#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --account=def-kleinke
#SBATCH --nodes=1
#SBATCH --gpus-per-node=h100:1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=4
#SBATCH --job-name=BaLaCuSe3_dos
#SBATCH --mail-type=ALL
#SBATCH --mail-user=royhe62@yahoo.ca
#SBATCH --output=BaLaCuSe3_dos-output.txt
#SBATCH --error=BaLaCuSe3_dos-errors.txt

module purge

module load StdEnv/2023
module load gcc/12.3
module load openmpi/4.1.5
module load gromacs/2025.4
module load apptainer/1.2.4
module load cuda/12.6

echo "Hello!"

i=1
max_jobs=4
running=0

while IFS= read -r config_name <&3; do
    srun --exclusive -N1 -n1 apptainer exec --nv \
        /home/royhe62/scratch/sifs/hcnn.sif \
        conda run --no-capture-output -n HCNN \
        python code/classification/train.py \
        -c "classification/config/${config_name}" \
        > "outputs/Incexp_${i}.txt" 2>&1 &

    ((i++))
    ((running++))

    # Wait after launching 4 jobs
    if (( running == max_jobs )); then
        wait
        running=0
    fi

done 3< config_list_inc.txt

# Wait for any remaining jobs
wait