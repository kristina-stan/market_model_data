from pdf2image import convert_from_path
import os
from .file_helpers import safe_mkdir

def extract_pdf_pages(pdf_path: str, output_folder: str, dpi=300):
    """
    Convert PDF pages to PNG images saved under output_folder.
    Returns list of saved image file paths.
    """
    safe_mkdir(output_folder)
    pages = convert_from_path(pdf_path, dpi=dpi)
    saved_files = []

    for i, page in enumerate(pages, start=1):
        img_filename = f"page_{i}.png"
        img_path = os.path.join(output_folder, img_filename)
        page.save(img_path, format="PNG")
        saved_files.append(img_path)

    return saved_files

def pdf_to_images(pdf_path, dpi=300):
    try:
        return convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
        return None
