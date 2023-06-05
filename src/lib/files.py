import os

from glob import glob
from .path import get_file_stem
from .run import Run

ROOT_FILES_DIR = os.environ["ROOT_FILES_DIR"]

def get_root_files_in_dir(dir=ROOT_FILES_DIR):
    if not os.path.isdir(dir):
        raise ValueError(f"Tried to get root files in dir '{dir}' but path provided is not a directory.")
    files = glob(os.path.join(dir, '*.root'))
    return files

def root_files_to_runs(dir=ROOT_FILES_DIR) -> list[Run]:
    data = [(get_file_stem(path), path) for path in get_root_files_in_dir(dir)]
    data.sort(key=lambda tuple: tuple[1])
    runs = map(lambda data: Run(name=data[0], path=data[1]), data)
    return list(runs)