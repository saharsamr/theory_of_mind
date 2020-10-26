import numpy as np
from scipy import stats

from collections import defaultdict


N_TRIALS = 300
DIFF = 5


def vectorize_differences(subjects_coefficients, window_size, diff, growing_window=True):

    vectorized_differences = {
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

    if growing_window:
        for model_key in vectorized_differences.keys():
            for coef in vectorized_differences[model_key].keys():
                for end in range(50, N_TRIALS, diff):
                    for id, subject_coefs in subjects_coefficients.items():

                        point_key = (0, end)
                        vectorized_differences[model_key][coef][point_key].append(\
                            subject_coefs[model_key][point_key][coef] - subject_coefs[model_key][(0, N_TRIALS)][coef])
    else:
        for model_key in vectorized_differences.keys():
            for coef in vectorized_differences[model_key].keys():
                for start in range(0, N_TRIALS-window_size, diff):
                    for id, subject_coefs in subjects_coefficients.items():

                        point_key = (start, start+window_size)
                        vectorized_differences[model_key][coef][point_key].append(\
                            subject_coefs[model_key][point_key][coef] - subject_coefs[model_key][(0, N_TRIALS)][coef])

    return vectorized_differences


def calc_difference_means_with_error_bar(subjects_coefficients, window_size, diff):

    vectorized_differences = vectorize_differences(subjects_coefficients, window_size, diff)

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

    for model_key in vectorized_differences.keys():
        for coef in vectorized_differences[model_key].keys():
            for point_key, values in vectorized_differences[model_key][coef].items():

                differences_data[model_key][coef][point_key] = {
                    'mean': np.mean(values),
                    'se': np.std(values) / np.sqrt(len(values))
                }

    return differences_data, vectorized_differences


def t_test_on_differences(vectorize_differences):

    t_test_results = {
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

    for model_key in vectorize_differences.keys():
        for coef in vectorize_differences[model_key].keys():
            for point_key, values in vectorize_differences[model_key][coef].items():

                T = stats.ttest_ind(values, [0 for v in values])
                t_test_results[model_key][coef][point_key] = {
                    'statistic':  T.statistic,
                    'pvalue': T.pvalue
                }

    return t_test_results
