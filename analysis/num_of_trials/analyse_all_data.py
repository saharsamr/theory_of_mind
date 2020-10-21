import numpy as np

from collections import defaultdict


N_TRIALS = 300
DIFF = 5


def vectorize_data(subjects_coefficients, window_size, diff):

    vectorized_data = {
        'model_free': {
            'common_reward': defaultdict(list),
            'unique_reward': defaultdict(list),
            'interaction': defaultdict(list)
        },
        'model_based': {
            'common_reward': defaultdict(list),
            'reward_prob': defaultdict(list),
            'interaction': defaultdict(list)
        }
    }

    for model_key in vectorized_data.keys():
        for coef in vectorized_data[model_key].keys():
            for start in range(0, N_TRIALS-window_size, diff):
                for id, subject_coefs in subjects_coefficients.items():

                    point_key = (start, start+window_size)
                    vectorized_data[model_key][coef][point_key].append(subject_coefs[model_key][point_key][coef])

    return vectorized_data


def calc_difference_means_with_error_bar(subjects_coefficients, window_size, diff):

    vectorized_data = vectorize_data(subjects_coefficients, window_size, diff)

    differences_data = {
        'model_free': {
            'common_reward': {},
            'unique_reward': {},
            'interaction': {}
        },
        'model_based': {
            'common_reward': {},
            'reward_prob': {},
            'interaction': {}
        }
    }

    for model_key in vectorized_data.keys():
        for coef in vectorized_data[model_key].keys():
            for point_key, values in vectorized_data[model_key][coef].items():

                differences_data[model_key][coef][point_key] = {
                    'mean': np.mean(values),
                    'se': np.std(values) / np.sqrt(len(values))
                }

    return differences_data
