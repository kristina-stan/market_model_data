import re

def sanitize_filename(name: str) -> str:
    """Replace invalid filename characters with underscores."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def clean_text(text: str) -> str:
    """Clean text from unwanted spaces or control characters."""
    return text.strip()
