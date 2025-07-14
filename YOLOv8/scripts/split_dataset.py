import os
import random
import shutil

#---------- ORGANISES THE DATASET ----------

# flyers_images_labels -> sorted_images_labels/images and sorted_images_labels/labels
def collect_from_flyers(flyers_folder='../data/flyers_images_labels', all_folder='../data/sorted_images_labels'):
    images_dst = os.path.join(all_folder, 'images')
    labels_dst = os.path.join(all_folder, 'labels')
    os.makedirs(images_dst, exist_ok=True)
    os.makedirs(labels_dst, exist_ok=True)

    for root, dirs, files in os.walk(flyers_folder):
        if 'sorted_images_labels' in root:
            continue
        for file in files:
            src = os.path.join(root, file)
            if file.endswith('.png'):
                shutil.copy2(src, os.path.join(images_dst, file))
            elif file.endswith('.txt'):
                shutil.copy2(src, os.path.join(labels_dst, file))


def split_data(
    all_images_dir='../data/sorted_images_labels/images',
    all_labels_dir='../data/sorted_images_labels/labels',
    output_base='../data',
    train_ratio=0.8,
    seed=42
):
    random.seed(seed)

    all_images = [f for f in os.listdir(all_images_dir) if f.endswith('.png')]
    random.shuffle(all_images)

    split_index = int(len(all_images) * train_ratio)
    train_images = all_images[:split_index]
    val_images = all_images[split_index:]

    image_train_dir = os.path.join(output_base, 'images', 'train')
    image_val_dir = os.path.join(output_base, 'images', 'val')
    label_train_dir = os.path.join(output_base, 'labels', 'train')
    label_val_dir = os.path.join(output_base, 'labels', 'val')

    for d in [image_train_dir, image_val_dir, label_train_dir, label_val_dir]:
        os.makedirs(d, exist_ok=True)

    def copy_files(image_list, image_dst, label_dst):
        for image_name in image_list:
            base_name = os.path.splitext(image_name)[0]
            label_name = base_name + '.txt'

            image_src = os.path.join(all_images_dir, image_name)
            label_src = os.path.join(all_labels_dir, label_name)

            image_dst_path = os.path.join(image_dst, image_name)
            label_dst_path = os.path.join(label_dst, label_name)

            shutil.copy2(image_src, image_dst_path)

            if os.path.exists(label_src):
                shutil.copy2(label_src, label_dst_path)
            else:
                print(f"[WARN] Label not found for image: {image_name}")

    copy_files(train_images, image_train_dir, label_train_dir)
    copy_files(val_images, image_val_dir, label_val_dir)

    print(f"[DONE] Split: {len(train_images)} train / {len(val_images)} val")


if __name__ == '__main__':
    collect_from_flyers()
    split_data()
