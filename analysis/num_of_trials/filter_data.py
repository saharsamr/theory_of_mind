from tools.directory_files import get_file_names
from tools.load_mat import load_mat

from collections import defaultdict

import numpy as np


N_TRIALS = 300


def filtered_data(path):

    filtered_data = defaultdict(dict)

    data_files = get_file_names(path)
    data_files = ['data/' + file for file in data_files]
    for file in data_files:

        data = load_mat(file)
        if data['has_conf'] == False:

            id = data['ID'][0][0]
            filtered_data[id] = {
                'chosen': data['chosen'].transpose().reshape(1, N_TRIALS)[0].astype(np.int64),
                'realized_reward': data['Subject']['realized_reward'][0][0],
                'outcome': data['Subject']['outcome_mat'][0][0].astype(np.int64),
                'no_reverse': data['Subject']['Format'][0][0],
                'trials': data['Subject']['Trials'][0][0].astype(np.int64),
                'reward_probs': data['Subject']['reward_prob'][0][0]
            }

    return filtered_data
