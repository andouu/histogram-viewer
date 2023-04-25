from os import path
from glob import glob
from .path import get_file_stem

ROOT_FILES_DIR = "/Users/andou/Documents/Pioneer/midas-stuff/midas_to_root/output/root/1313-1330"

def get_root_files_in_dir(dir=ROOT_FILES_DIR):
    if not path.isdir(dir):
        raise ValueError(f"Tried to get root files in dir '{dir}' but path provided is not a directory.")
    files = glob(path.join(dir, '*.root'))
    return files

def get_default_root_files():
    data = [(get_file_stem(path), path) for path in get_root_files_in_dir()]
    data.sort(key=lambda tuple: tuple[1])

    return data