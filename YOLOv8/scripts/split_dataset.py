from pdf2image import convert_from_path
import os

# Input paths
input_dirs = {
    "kaufland": "../../process/kaufland/downloads",
    "lidl": "../../process/lidl/downloads"
}

# Output folder
output_folder = "../data/flyers"
os.makedirs(output_folder, exist_ok=True)

def extract_pages(store_name, source_dir):
    for filename in os.listdir(source_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(source_dir, filename)
        base_name = os.path.splitext(filename)[0]  # no .pdf

        print(f"[{store_name.upper()}] Processing: {filename}")

        try:
            pages = convert_from_path(pdf_path, dpi=300)
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
            continue

        flyer_folder = os.path.join(output_folder, store_name, base_name)
        os.makedirs(flyer_folder, exist_ok=True)

        print("Saving pages...")
        for i, page in enumerate(pages, start=1):
            img_filename = f"page_{i}.png"
            page_path = os.path.join(flyer_folder, img_filename)
            try:
                page.save(page_path, format="PNG")
            except Exception as e:
                print(f"Failed to save page {img_filename}: {e}")

        print(f"[{store_name.upper()}] Done: {filename}\n")

    print(f"[{store_name.upper()}] All PDFs processed.\n")

def main():
    for store_name, path in input_dirs.items():
        extract_pages(store_name, path)

if __name__ == "__main__":
    main()
