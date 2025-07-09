from pdf2image import convert_from_path
import os

# Path to your PDF
flyers_origin = "D:/SIS_Technology/python_scripts/agent_better/kaufland/downloads"
output_folder = "flyers"

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(flyers_origin):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(flyers_origin, filename)
        base_name = os.path.basename(filename)

        print(f"Processing {filename}...")

        # Convert PDF to images
        pages = convert_from_path(pdf_path, dpi=300)
        print("Converted!")

        # Create a subfolder for this flyer
        flyer_folder = os.path.join(output_folder, base_name)
        os.makedirs(flyer_folder, exist_ok=True)

        # Save each page with a unique filename
        print("Saving pages...")
        for i, page in enumerate(pages):
            img_filename = f"page_{i + 1}.png"
            page.save(os.path.join(flyer_folder, img_filename), "PNG")

print("All PDFs converted to images.")
