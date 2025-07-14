# train.py
import split_dataset
from ultralytics import YOLO

if __name__ == '__main__':
    split_dataset.collect_from_flyers()
    split_dataset.split_data()

    # FOR A NEW MODEL
    model = YOLO('../models/types/yolov8x.pt')  # or yolov8n/s/m/l/x.pt

    # FOR UPDATING THE KNOWLEDGE OF A MODEL (new+old images, same weights)
    #model = YOLO('../models/trained/train1/weights/best.pt')
    model.train(
        data='../product_blocks.yaml',
        epochs=50,
        project='../models/trained',
        name='train1'
    )
