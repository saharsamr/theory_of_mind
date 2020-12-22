from task.params.task_params import TaskParams
from tools.directory_files import get_directory_names

from analysis.glmfit import fit_binomial_glm as glmfit
from analysis.glmfit import fit_mixed_lm as mixedlm

import numpy as np
import pandas as pd
from scipy.stats import sem

import json


def extract_MF_probabilities(data_path):

    subjectd_IDs = get_directory_names(data_path)
    c1u1s, c1u0s, c0u1s, c0u0s = [], [], [], []
    for id in subjectd_IDs:

        repeat, common_rewarded, unique_rewarded = extract_MF_behavior_data(data_path, id)
        common1_unique0, common0_unique1, common0_unique0, common1_unique1 = \
            find_repeat_probs(repeat, common_rewarded, unique_rewarded)

        c1u1s.append(common1_unique1)
        c1u0s.append(common1_unique0)
        c0u1s.append(common0_unique1)
        c0u0s.append(common0_unique0)

    return np.mean(c1u1s), sem(c1u1s), np.mean(c1u0s), sem(c1u0s),\
        np.mean(c0u1s), sem(c0u1s), np.mean(c0u0s), sem(c0u0s)


def extract_data_MF_glmfit(data_path):

    pulled_dataframe = pd.DataFrame({'repeat': [], 'common_reward': [], 'unique_reward':[], 'subject_id': []})
    subject_models, subject_results, pulled_model, pulled_results = [], [], None, None

    subjectd_IDs = get_directory_names(data_path)
    for id in subjectd_IDs:
        model, result, subject_df = glmfit_for_single_subject(data_path, id)
        subject_models.append(model)
        subject_results.append(result)
        pulled_dataframe = pulled_dataframe.append(subject_df, ignore_index=True)

    pulled_model, pulled_results = mixedlm(
        pulled_dataframe,
        'repeat ~ common_reward*unique_reward',
        {'a': '0+C(subject_id)', 'b': '0+C(subject_id)*common_reward', 'c': '0+C(subject_id)*unique_reward'}
    )

    return subject_models, subject_results, pulled_model, pulled_results


def glmfit_for_single_subject(data_path, id):
    repeat, common_rewarded, unique_rewarded = extract_MF_behavior_data(data_path, id)
    subject_dataframe = pd.DataFrame({
        'repeat': repeat,
        'common_reward': common_rewarded,
        'unique_reward': unique_rewarded,
        'subject_id': [int(id) for _ in repeat]
    })
    model, result = glmfit(subject_dataframe, formula='repeat ~ common_reward*unique_reward')
    return model, result, subject_dataframe


def extract_MF_behavior_data(data_path, subject_id):

    with open('{}{}/{}-task-phase2.json'.format(data_path, subject_id,subject_id), 'r') as data_file:

        last_pair_in_block = lambda index: \
            index%TaskParams.num_of_block_trials == TaskParams.num_of_block_trials-1

        data = json.load(data_file)
        repeat, common_rewarded, unique_rewarded = [], [], []
        for block in range(TaskParams.n_agent_blocks):
            for i, (pre_trial, trial) in enumerate(zip(
                data[block*TaskParams.n_agent_block_trials:(block+1)*TaskParams.n_agent_block_trials-1],
                data[block*TaskParams.n_agent_block_trials+1:(block+1)*TaskParams.n_agent_block_trials]
            )):
                if pre_trial['selected_option'] in trial['options']:

                    repeat.append(1 if pre_trial['selected_option'] == trial['selected_option'] else 0)

                    common_reward, unique_reward = extract_common_unique_reward_status(pre_trial, trial)
                    common_rewarded.append(common_reward)
                    unique_rewarded.append(unique_reward)

    return repeat, common_rewarded, unique_rewarded


def find_repeat_probs(repeat, common_rewarded, unique_rewarded):

    calc_prob = lambda values: sum(values)/len(values)

    repeat = np.array(repeat)
    common_rewarded, unique_rewarded = np.array(common_rewarded), np.array(unique_rewarded)

    common1_unique0 = np.where((common_rewarded == 1) & (unique_rewarded == 0))
    common1_unique0_repeat_prob = calc_prob(repeat[common1_unique0])

    common0_unique1 = np.where((common_rewarded == 0) & (unique_rewarded == 1))
    common0_unique1_repeat_prob = calc_prob(repeat[common0_unique1])

    common0_unique0 = np.where((common_rewarded == 0) & (unique_rewarded == 0))
    common0_unique0_repeat_prob = calc_prob(repeat[common0_unique0])

    common1_unique1 = np.where((common_rewarded == 1) & (unique_rewarded == 1))
    common1_unique1_repeat_prob = calc_prob(repeat[common1_unique1])

    return common1_unique0_repeat_prob, common0_unique1_repeat_prob, common0_unique0_repeat_prob, common1_unique1_repeat_prob


def extract_common_unique_reward_status(pre_trial, trial):

    difference = lambda pair, object: pair[0] if object != pair[0] else pair[1]

    visited_pair = pre_trial['visited_objects']
    other_pair = difference(pre_trial['possible_objects'], visited_pair)

    common, unique = find_common_unique(trial['possible_objects'][0], trial['possible_objects'][1], visited_pair)

    common_index = 0 if common == visited_pair[0] else 1
    common_reward = int(pre_trial['gained_rewards'][common_index])
    unique_reward = int(pre_trial['gained_rewards'][1-common_index])

    return common_reward, unique_reward


def find_common_unique(first_pair, second_pair, visited_pair):

    common, unique = None, None
    for object in first_pair:
        if object in second_pair:
            common = object
            break

    unique = visited_pair[0] if common != visited_pair[0] else visited_pair[1]

    return common, unique
