import os, random, shutil

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def move_files(image_list, all_images_dir, all_labels_dir, dest_img_dir, dest_lbl_dir):
    for img_file in image_list:
        label_file = img_file.replace('.png', '.txt')

        img_src = os.path.join(all_images_dir, img_file)
        lbl_src = os.path.join(all_labels_dir, label_file)

        if os.path.exists(lbl_src):
            shutil.copy(img_src, os.path.join(dest_img_dir, img_file))
            shutil.copy(lbl_src, os.path.join(dest_lbl_dir, label_file))
        else:
            print(f"⚠️ Label missing for {img_file}, skipping.")

def split_data():
    #random.seed(42)

    all_images_dir = '../data/all_images'
    all_labels_dir = '../data/all_labels'

    output_images_train = '../data/images/train'
    output_labels_train = '../data/labels/train'
    output_images_val = '../data/images/val'
    output_labels_val = '../data/labels/val'

    os.makedirs(output_images_train, exist_ok=True)
    os.makedirs(output_labels_train, exist_ok=True)
    os.makedirs(output_images_val, exist_ok=True)
    os.makedirs(output_labels_val, exist_ok=True)

    clear_folder(output_images_train)
    clear_folder(output_labels_train)
    clear_folder(output_images_val)
    clear_folder(output_labels_val)

    image_files = [f for f in os.listdir(all_images_dir) if f.endswith('.png')]
    random.shuffle(image_files)

    # Split 80% train, 20% val
    split_idx = int(len(image_files) * 0.8)
    train_images = image_files[:split_idx]
    val_images = image_files[split_idx:]

    move_files(train_images, all_images_dir, all_labels_dir, output_images_train, output_labels_train)
    move_files(val_images, all_images_dir, all_labels_dir, output_images_val, output_labels_val)

    print(f"Done! {len(train_images)} images for training, {len(val_images)} for validation.")
    return len(train_images), len(val_images)

# Optional: run directly
if __name__ == "__main__":
    split_data()
