from os import listdir
from os.path import isfile, join


def get_file_names(dir_path, extention=None):

    if extention:
        file_names = [f for f in listdir(dir_path) if f.endswith('.' + extension)]
    else:
        file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
        
    return file_names
