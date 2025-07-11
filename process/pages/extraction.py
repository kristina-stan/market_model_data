import os
from utils import create_folder_if_not_exists
from utils import pdf_to_images

# Input paths
input_dirs = {
    "kaufland": "..\kaufland\downloads",
    "lidl": "..\lidl\downloads"
}

output_folder = "flyers"
create_folder_if_not_exists(output_folder)

def extract_pages(store_name, source_dir):
    for filename in os.listdir(source_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(source_dir, filename)
        base_name = os.path.splitext(filename)[0]  # no .pdf

        print(f"[{store_name.upper()}] Processing: {filename}")

        pages = pdf_to_images(pdf_path)
        if pages is None:
            continue

        flyer_folder = os.path.join(output_folder, store_name, base_name)
        create_folder_if_not_exists(flyer_folder)

        print("Saving pages...")
        for i, page in enumerate(pages, start=1):
            img_filename = f"page_{i}.png"
            page_path = os.path.join(flyer_folder, img_filename)
            page.save(page_path, format="PNG")

        print(f"[{store_name.upper()}] Done: {filename}\n")

    print(f"[{store_name.upper()}] All PDFs processed.\n")

def main():
    for store_name, path in input_dirs.items():
        extract_pages(store_name, path)

if __name__ == "__main__":
    main()
