# this is the process init

from utils.file_helpers import create_folder_if_not_exists
from .core.finder import find_magazine_test
from .core.testerr import get_image_urls

__all__ = ['create_folder_if_not_exists', 'find_magazine_test', 'get_image_urls']