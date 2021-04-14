#!/bin/bash
#SBATCH --job-name=aabir-extract-all
#SBATCH --output=/project2/jevans/aabir/NOWwhat/logs/extract_apr_14.out
#SBATCH --error=/project2/jevans/aabir/NOWwhat/logs/extract_apr_14.err
#SBATCH --partition=broadwl
#SBATCH --mem=31GB
#SBATCH --time=32:00:00

#module load Anaconda3/5.3.0

echo 'run started at $(date)'
python /project2/jevans/aabir/NOWwhat/datascripts/extract_all.py
echo 'run ended at $(date)'
