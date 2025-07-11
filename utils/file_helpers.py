import os

def safe_mkdir(path: str):
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)

def safe_write_bytes(file_path: str, data: bytes):
    """Write bytes to file safely."""
    safe_mkdir(os.path.dirname(file_path))
    with open(file_path, "wb") as f:
        f.write(data)

def list_pdf_files(directory: str):
    """Return a list of PDF filenames in the directory."""
    return [f for f in os.listdir(directory) if f.lower().endswith(".pdf")]

def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
