import os
import time
import random
import ROOT

from os import path
from glob import glob
from pprint import pprint

ROOT_FILES_DIR = "/Users/andou/Documents/Pioneer/midas-stuff/midas_to_root/output/root/1313-1330"

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

def main():
    t_file = ROOT.TFile.Open(root_files[0][1])
    drs0_tree = t_file.Get("DRS0 (EVENT ID = 1)")
    arr = []
    for i, event in enumerate(drs0_tree):
        charges = event.charge
        arr.append(charges)
        print(f"Processed: {i + 1}")

    uniq_vec = set() 

    for i, vec in enumerate(arr):
        uniq_vec.add(arr[i])
        print(i)
        
        
    pprint(uniq_vec)

if __name__ == "__main__":
    main()