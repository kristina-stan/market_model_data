import os

data_path = "data"
for split in ["train", "val"]:
    img_dir = os.path.join(data_path, "images", split)
    lbl_dir = os.path.join(data_path, "labels", split)

    img_files = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])
    lbl_files = sorted([f for f in os.listdir(lbl_dir) if f.endswith(".txt")])

    print(f"{split} images: {len(img_files)}")
    print(f"{split} labels: {len(lbl_files)}")

    missing_labels = [f for f in img_files if f.replace(".png", ".txt") not in lbl_files]
    if missing_labels:
        print(f"Missing label files for {split}: {missing_labels[:5]}")
    else:
        print(f"All {split} images have labels.")
