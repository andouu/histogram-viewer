import os
import ROOT

from os import path
from glob import glob
from pprint import pprint

ROOT_FILES_DIR = "/Users/andou/Documents/Pioneer/midas-stuff/midas_to_root/output/root/test"

def get_file_stem(path):
    if not os.path.exists(path):
        raise ValueError(f"Path '{path}' does not exist!")
    return os.path.basename(path).split('.')[0]

def get_root_files_in_dir(dir=ROOT_FILES_DIR):
    if not path.isdir(dir):
        raise ValueError(f"Tried to get root files in dir '{dir}' but path provided is not a directory.")
    files = glob(path.join(dir, '*.root'))
    return files

def get_default_root_files():
    data = [(get_file_stem(path), path) for path in get_root_files_in_dir()]
    data.sort(key=lambda tuple: tuple[1])

    return data

root_files = get_default_root_files()

t_files = [ROOT.TFile.Open(run[1], "r") for run in root_files]

def main():
    t_file = t_files[0]
    inpt_tree = t_file.Get("INPT")
    print(inpt_tree.GetEntries())
    histogram = t_file.Get("channel_1_histogram")
    print(histogram.GetEntries())

if __name__ == "__main__":
    main()