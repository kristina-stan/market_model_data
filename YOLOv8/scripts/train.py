# train.py
import split_dataset
from ultralytics import YOLO

if __name__ == '__main__':
    split_dataset.split_data()

    model = YOLO('../models/yolov8l.pt')  # or yolov8n/s/m/l/x.pt

    model.train(
        data='../product_blocks.yaml',  # relative path to dataset YAML
        epochs=50,
        project='E:/SIS_Technology/market_model_data/YOLOv8',
        name='train1',
        device=0
    )
