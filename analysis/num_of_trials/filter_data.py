from tools.directory_files import get_file_names
from tools.load_mat import load_mat

from collections import defaultdict


def filter_data(path):

    filtered_data = defaultdict(dict)

    data_files = get_file_names(path)
    data_files = ['data/' + file for file in data_files]
    for file in data_files:

        data = load_mat(file)
        if data['has_conf'] == False:

            id = data['ID'][0][0]
            filtered_data[id] = {
                'chosen': data['chosen'],
                'realized_reward': data['Subject']['realized_reward'],
                'outcome': data['Subject']['outcome_mat'],
                'no_reverse': data['Subject']['Format'],
                'trials': data['Subject']['Trials']
            }

    return filtered_data
