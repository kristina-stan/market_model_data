import os
import cv2
import numpy as np
from ultralytics import YOLO

# ---------------------- Configuration ----------------------

# Path to trained model weights
MODEL_PATH = '../train12/weights/last.pt'
# Path to validation images
VAL_IMAGES_DIR = '../data/images/val'

# Max window size for display
MAX_WIDTH = 1280
MAX_HEIGHT = 720

# Confidence threshold for displaying detections (optional)
CONFIDENCE_THRESHOLD = 0.25

# -----------------------------------------------------------

def resize_to_fit(img, max_w, max_h):
    """Resize image to fit max dimensions while preserving aspect ratio."""
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h))


def draw_detections(img, boxes, scores, classes):
    """Draw bounding boxes, class labels, and contours on the image."""
    for box, score, cls in zip(boxes, scores, classes):
        if score < CONFIDENCE_THRESHOLD:
            continue

        x1, y1, x2, y2 = box.astype(int)

        # Draw bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        # Class and confidence label
        label = f"{cls}: {score:.2f}"
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Optional: Draw a polygon contour around the box
        contour = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
        cv2.drawContours(img, [contour], -1, (0, 0, 255), 2)


def main():
    # Load trained YOLOv8 model
    model = YOLO(MODEL_PATH)

    # List sorted_images_labels image files in validation folder
    image_files = [f for f in os.listdir(VAL_IMAGES_DIR) if f.lower().endswith('.png')]

    for img_name in image_files:
        img_path = os.path.join(VAL_IMAGES_DIR, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"[WARNING] Failed to load image: {img_path}")
            continue

        # Perform inference
        results = model(img)
        result = results[0]

        # Extract boxes, confidence scores, and class IDs
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy().astype(int)

        # Draw detections on image
        draw_detections(img, boxes, scores, classes)

        # Resize and show image
        img_resized = resize_to_fit(img, MAX_WIDTH, MAX_HEIGHT)
        cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
        cv2.imshow("Detection", img_resized)
        cv2.waitKey(0)  # Press any key to show next image

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
