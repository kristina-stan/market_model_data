import os, asyncio, fitz
from utils import safe_mkdir, list_pdf_files

input_folder = "data/downloads" # pdfs_folder
output_folder = "data/pages" # pages_folder

async def save_all_pdfs_as_images():
    print("Saving the pages...")
    for shop_name in os.listdir(input_folder):
        print('in for')
        shop_path = os.path.join(input_folder, shop_name)
        if not os.path.isdir(shop_path):
            continue  # Skip non-folder entries

        pdf_files = list_pdf_files(shop_path)
        for pdf_file in pdf_files:
            pdf_path = os.path.join(shop_path, pdf_file)
            pdf_basename = os.path.splitext(pdf_file)[0]
            output_subfolder = os.path.join(output_folder, shop_name, pdf_basename)
            safe_mkdir(output_subfolder)

            print(f"[•] Converting: {pdf_path} → {output_subfolder}")
            doc = fitz.open(pdf_path)

            for page_number in range(len(doc)):
                page = doc.load_page(page_number)
                pix = page.get_pixmap(dpi=200)
                output_file = os.path.join(output_subfolder, f"page_{page_number + 1}.png")
                pix.save(output_file)
                print(f"[✓] Saved page {page_number + 1} → {output_file}")

            doc.close()

if __name__ == "__main__":
    asyncio.run(save_all_pdfs_as_images())
