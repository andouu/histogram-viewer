import os

def get_file_stem(path):
    if not os.path.exists(path):
        raise ValueError(f"Path '{path}' does not exist!")
    return os.path.basename(path).split('.')[0]