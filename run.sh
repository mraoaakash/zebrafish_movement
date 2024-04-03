#! /bin/bash
#PBS -N Zebrafish_Movement
#PBS -o Zebrafish_Movement_out.log
#PBS -e Zebrafish_Movement_err.log
#PBS -l ncpus=100
#PBS -q cpu

# eval "$(conda shell.bash hook)"
# conda activate zebrafish_movement


# cd /storage/aakash.rao_asp24/research/research-zebrafish/zebrafish_movement/
# python3 larval/train_script.py \
#     --data /storage/aakash.rao_asp24/research/research-zebrafish/zebrafish_movement/larval/data.yaml  \
#     --epochs 25  \
#     --imgsz 1920  \
#     --name Larval-Run  \
#     --batch 8  \
#     --save_period 2 \
#     --device mps,  \
#     --rect True  \
#     --workers 0 \

python3 larval/test_script.py \
    --video_path /Users/mraoaakash/Documents/research/research-zebrafish/data/videos/processed_use \
    --pre_post pre \
    --modelpath /Users/mraoaakash/Documents/research/research-zebrafish/Movement/zebrafish_movement/runs/Larval-Run/weights/epoch12.pt \
    --savepath /Users/mraoaakash/Documents/research/research-zebrafish/data/videos/tracked \
    --outpath /Users/mraoaakash/Documents/research/research-zebrafish/data/videos/overlay \

cd /storage/aakash.rao_asp24/research/research-zebrafish/zebrafish_movement

# python3 larval/test_script.py \
#     --video_path /storage/aakash.rao_asp24/research/research-zebrafish/data/videos/processed_use \
#     --pre_post pre \
#     --modelpath /storage/aakash.rao_asp24/research/research-zebrafish/zebrafish_movement/runs/detect/Larval-Run/weights/epoch12.pt \
#     --savepath /storage/aakash.rao_asp24/research/research-zebrafish/data/videos/tracked \
#     --outpath /storage/aakash.rao_asp24/research/research-zebrafish/data/videos/overlay \
