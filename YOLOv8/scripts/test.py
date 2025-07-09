
from ultralytics import YOLO
import cv2
import os
import numpy as np

# Maximum display width and height (adjust to fit your monitor)
max_width = 1280
max_height = 720

# Resize image function with aspect ratio preservation
def resize_to_fit(img, max_w, max_h):
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h))

# Load your trained model (adjust path if needed)
model = YOLO('/app/YOLOv8/train1/weights/last.pt')

# Path to your validation images folder
val_images_path = '/app/YOLOv8/data/images/val'

# List all image files in val folder
image_files = [f for f in os.listdir(val_images_path) if f.endswith('.png')]

for img_name in image_files:
    img_path = os.path.join(val_images_path, img_name)
    img = cv2.imread(img_path)

    # Run prediction
    results = model(img)

    # results[0] is a ultralytics.yolo.engine.results.Results object
    # It contains boxes, masks, probs, etc.

    boxes = results[0].boxes.xyxy.cpu().numpy()  # bounding boxes in xyxy format
    scores = results[0].boxes.conf.cpu().numpy()  # confidence scores
    classes = results[0].boxes.cls.cpu().numpy().astype(int)  # class IDs

    # Draw bounding boxes and labels on image using contours
    for (box, score, cls) in zip(boxes, scores, classes):
        x1, y1, x2, y2 = box.astype(int)

        # Draw rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

        # Put label text
        label = f"{cls}: {score:.2f}"
        cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 3)

        # Create contour from box corners to visualize as a polygon (optional)
        pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
        cv2.drawContours(img, [pts], 0, (0,0,255), 3)

    # Show image with detections
    cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
    img_resized = resize_to_fit(img, max_width, max_height)
    cv2.imshow('Detection', img)
    cv2.waitKey(0)  # Wait for key press to show next image

cv2.destroyAllWindows()
