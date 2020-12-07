from os import listdir
from os.path import isfile, join, isdir


def get_file_names(dir_path, extention=None):

    if extention:
        file_names = [f for f in listdir(dir_path) if f.endswith('.' + extention)]
    else:
        file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    return file_names


def get_directory_names(dir_path):

    dir_names = [dir for dir in listdir(dir_path)]

    return dir_names
