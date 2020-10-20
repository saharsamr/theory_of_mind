from analysis.num_of_trials.extract_info import extract_subject_trials_info
from analysis.num_of_trials.glmfit import fit_binomial_glm

import numpy as np


N_TRIALS = 300


def analyse_trials(subject_filtered_data, repeat_probs, start_index=0, end_index=N_TRIALS):

    model_free_data, model_based_data = extract_subject_trials_info(subject_filtered_data, start_index)

    repeat_mf_probs = calc_repeat_probs_MF(model_free_data)
    repeat_mb_probs = calc_repeat_probs_MB(model_based_data)
    repeat_probs['model_free'][(start_index, end_index)] = repeat_mf_probs
    repeat_probs['model_based'][(start_index, end_index)] = repeat_mb_probs

    mf_model, mf_result = fit_binomial_glm(model_free_data, formula='repeat ~ common_reward*unique_reward')
    mb_model, mb_result = fit_binomial_glm(model_based_data, formula='repeat ~ common_reward*reward_prob')

    return repeat_probs


def get_trials_subset(subject_filtered_data, start_index, end_index):

    result = {
        'chosen': subject_filtered_data['chosen'][start_index:end_index],
        'realized_reward': subject_filtered_data['realized_reward'][start_index:end_index],
        'outcome': subject_filtered_data['outcome'],
        'trials': subject_filtered_data['trials'][start_index:end_index],
        'reward_probs': subject_filtered_data['reward_probs'][start_index:end_index]
    }
    return result


def analyse_with_moving_window(subject_filtered_data, window_size, diff, repeat_probs):

    for start in range(0, N_TRIALS-window_size, diff):
        subset_filtered_data = get_trials_subset(subject_filtered_data, start, start+window_size)
        repeat_probs = analyse_trials(subset_filtered_data, repeat_probs, start_index=start, end_index=start+window_size)

    return repeat_probs


def analyse_single_subject(subject_filtered_data, subject_ID, window_size, diff):

    repeat_probs = {
        'model_free': {},
        'model_based': {}
    }

    repeat_probs = analyse_trials(subject_filtered_data, repeat_probs)
    repeat_probs = analyse_with_moving_window(subject_filtered_data, window_size, diff, repeat_probs)

    return repeat_probs


def calc_repeat_probs_MF(mf_data):

    common1_unique1_indices = np.where((mf_data['common_reward'] == 1) & (mf_data['unique_reward'] == 1))[0]
    common1_unique0_indices = np.where((mf_data['common_reward'] == 1) & (mf_data['unique_reward'] == 0))[0]
    common0_unique1_indices = np.where((mf_data['common_reward'] == 0) & (mf_data['unique_reward'] == 1))[0]
    common0_unique0_indices = np.where((mf_data['common_reward'] == 0) & (mf_data['unique_reward'] == 0))[0]

    return {
        'common1_unique1': np.mean(mf_data['repeat'][common1_unique1_indices]),
        'common1_unique0': np.mean(mf_data['repeat'][common1_unique0_indices]),
        'common0_unique1': np.mean(mf_data['repeat'][common0_unique1_indices]),
        'common0_unique0': np.mean(mf_data['repeat'][common0_unique0_indices])
    }


def calc_repeat_probs_MB(mb_data):

    common1_indices = np.where(mb_data['common_reward'] == 1)[0]
    common0_indices = np.where(mb_data['common_reward'] == 0)[0]

    return {
        'common1': np.mean(mb_data['repeat'][common1_indices]),
        'common0': np.mean(mb_data['repeat'][common0_indices])
    }
