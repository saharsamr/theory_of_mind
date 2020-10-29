from analysis.num_of_trials.extract_info import extract_subject_trials_info, get_bad_trial_indices
from analysis.num_of_trials.glmfit import fit_binomial_glm
from analysis.num_of_trials.print_results import print_glm_results

import numpy as np


N_TRIALS = 300


def analyse_trials(subject_filtered_data, repeat_probs, coefficients, start_index=0, end_index=N_TRIALS):

    model_free_data, model_based_data = extract_subject_trials_info(subject_filtered_data, start_index)

    bad_mb_indices = get_bad_trial_indices(model_based_data)
    model_based_data = model_based_data.drop(bad_mb_indices)
    model_based_data.reset_index(drop=True, inplace=True)

    repeat_mf_probs = calc_repeat_probs_MF(model_free_data)
    repeat_mb_probs = calc_repeat_probs_MB(model_based_data)
    repeat_probs['model_free'][(start_index, end_index)] = repeat_mf_probs
    repeat_probs['model_based'][(start_index, end_index)] = repeat_mb_probs

    mf_model, mf_result, mb_model, mb_result = None, None, None, None
    if len(model_free_data):
        mf_model, mf_result = fit_binomial_glm(model_free_data, formula='repeat ~ common_reward*unique_reward')
    if len(model_based_data):
        mb_model, mb_result = fit_binomial_glm(model_based_data, formula='repeat ~ common_reward*reward_prob')

    coefficients = add_coefficients(coefficients, mf_result, mb_result, start_index, end_index)

    if start_index == 0 and end_index == N_TRIALS:
        print_glm_results(mf_result, mb_result)

    return repeat_probs, coefficients


def get_trials_subset(subject_filtered_data, start_index, end_index):

    result = {
        'chosen': subject_filtered_data['chosen'][start_index:end_index],
        'realized_reward': subject_filtered_data['realized_reward'][start_index:end_index],
        'outcome': subject_filtered_data['outcome'],
        'trials': subject_filtered_data['trials'][start_index:end_index],
        'reward_probs': subject_filtered_data['reward_probs'][start_index:end_index]
    }
    return result


def add_coefficients(coefficients, mf_result, mb_result, start_index=0, end_index=N_TRIALS):

    if mf_result:
        coefficients['model_free'][(start_index, end_index)] = {
            'common_reward': mf_result.params.get('common_reward[T.True]'),
            'unique_reward': mf_result.params.get('unique_reward[T.True]'),
            'interaction': mf_result.params.get('common_reward[T.True]:unique_reward[T.True]')
        }
    if mb_result:
        coefficients['model_based'][(start_index, end_index)] = {
            'common_reward': mb_result.params.get('common_reward[T.True]'),
            'reward_prob': mb_result.params.get('reward_prob'),
            'interaction': mb_result.params.get('common_reward[T.True]:reward_prob')
        }

    return coefficients


def analyse_with_moving_window(subject_filtered_data, window_size, diff, repeat_probs, coefficients):

    for start in range(0, N_TRIALS-window_size, diff):
        subset_filtered_data = get_trials_subset(subject_filtered_data, start, start+window_size)
        repeat_probs, coefficients = analyse_trials(subset_filtered_data, repeat_probs, coefficients, start, start+window_size)

    return repeat_probs, coefficients


def analyse_with_growing_window(subject_filtered_data, repeat_probs, coefficients, diff):

    for end in range(50, N_TRIALS, diff):
        subset_filtered_data = get_trials_subset(subject_filtered_data, 0, end)
        repeat_probs, coefficients = analyse_trials(subset_filtered_data, repeat_probs, coefficients, 0, end)

    return repeat_probs, coefficients


def analyse_single_subject(subject_filtered_data, subject_ID, window_size, diff):

    repeat_probs = {
        'model_free': {},
        'model_based': {}
    }

    coefficients = {
        'model_free': {},
        'model_based': {}
    }

    repeat_probs, coefficients = analyse_trials(subject_filtered_data, repeat_probs, coefficients)
    repeat_probs, coefficients = analyse_with_growing_window(subject_filtered_data, repeat_probs, coefficients, diff)

    return repeat_probs, coefficients


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
