#!/bin/bash
#SBATCH --job-name=ner
#SBATCH --output=/project2/jevans/aabir/NOWwhat/logs/ner.out
#SBATCH --error=/project2/jevans/aabir/NOWwhat/logs/ner.err
#SBATCH --partition=broadwl
#SBATCH --mem=31GB
#SBATCH --time=32:00:00

module load Anaconda3/5.3.0

echo 'run started at' $(date)
python /project2/jevans/aabir/NOWwhat/xscripts/ner.py
echo 'run ended at' $(date)
