#! /bin/bash
#PBS -N Zebrafish_Movement
#PBS -o Zebrafish_Movement_out.log
#PBS -e Zebrafish_Movement_err.log
#PBS -l ncpus=50
#PBS -q gpu
#PBS -l host=compute3

eval "$(conda shell.bash hook)"
conda activate zebrafish_movement


cd /storage/aakash.rao_asp24/research/research-zebrafish/zebrafish_movement/
python3 larval/train_script.py \
    --data /storage/aakash.rao_asp24/research/research-zebrafish/zebrafish_movement/larval/data.yaml  \
    --epochs 25  \
    --imgsz 1920  \
    --name Larval-Run  \
    --batch 8  \
    --save_period 2 \
    --device mps,  \
    --rect True  \
    --workers 0 \
    --project /storage/aakash.rao_asp24/research/research-zebrafish/zebrafish_movement/larval \