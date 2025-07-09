# train.py
from ultralytics import YOLO
import split_dataset

# Step 1: Split the data
split_dataset.split_data()

# Step 2: Train the model
model = YOLO('../models/yolov8s.pt')  # or yolov8s/m/l/x.pt

model.train(
    data='../product_blocks.yaml',  # relative path to dataset YAML
    epochs=50,
    project='D:/SIS_Technology/python_scripts/app/YOLOv8',
    name='train1'
)
