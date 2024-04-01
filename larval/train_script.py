import comet_ml
import sys
from ultralytics import YOLO
import argparse

def trainer(
        data, 
        epochs, 
        imgsz, 
        name, 
        batch, 
        save_period, 
        device, 
        rect, 
        workers
        ):
    model = YOLO('yolov8m.pt') 
    results = model.train(
        data=data,
        epochs=int(epochs), 
        imgsz=int(imgsz),
        name=name, 
        batch=int(batch),
        save_period=int(save_period),
        device='mps',
        rect=rect,
        workers=int(workers)
        )
    
if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('--data', type=str, help='data.yaml file path')
    argparse.add_argument('--epochs', type=int, help='number of epochs')
    argparse.add_argument('--imgsz', type=int, help='image size')
    argparse.add_argument('--name', type=str, help='name of the model')
    argparse.add_argument('--batch', type=int, help='batch size')
    argparse.add_argument('--save_period', type=int, help='save period')
    argparse.add_argument('--device', type=str, help='device', default='mps')
    argparse.add_argument('--rect', type=bool, help='rect')
    argparse.add_argument('--workers', type=int, help='workers')
    args = argparse.parse_args()
    trainer(args.data, args.epochs, args.imgsz, args.name, args.batch, args.save_period, args.device, args.rect, args.workers)