from task.params.task_params import TaskParams
from tools.directory_files import get_directory_names

from analysis.glmfit import fit_binomial_glm as glmfit
from analysis.glmfit import fit_mixed_lm as mixedlm

import numpy as np
import pandas as pd
from scipy.stats import sem

import json


def extract_MB_probabilities(data_path):

    subjectd_IDs = get_directory_names(data_path)
    c1s, c0s = [], []
    for id in subjectd_IDs:

        repeat, common_rewarded, _ = extract_MB_behavior_data(data_path, id)
        common1, common0 = find_repeat_probs(repeat, common_rewarded)

        c1s.append(common1)
        c0s.append(common0)

    return np.mean(c1s), sem(c1s), np.mean(c0s), sem(c0s)


def extract_data_MB_glmfit(data_path):

    pulled_dataframe = pd.DataFrame({'repeat': [], 'common_reward': [], 'reward_prob':[], 'subject_id': []})
    subject_models, subject_results, pulled_model, pulled_results = [], [], None, None

    subjectd_IDs = get_directory_names(data_path)
    for id in subjectd_IDs:
        model, result, subject_df = glmfit_for_single_subject(data_path, id)
        subject_models.append(model)
        subject_results.append(result)
        pulled_dataframe = pulled_dataframe.append(subject_df, ignore_index=True)

    pulled_model, pulled_results = mixedlm(
        pulled_dataframe,
        'repeat ~ common_reward*reward_prob',
        {'a': '0+C(subject_id)', 'b': '0+C(subject_id)*common_reward', 'c': '0+C(subject_id)*reward_prob'}
    )

    return subject_models, subject_results, pulled_model, pulled_results


def glmfit_for_single_subject(data_path, id):

    repeat, common_rewarded, reward_prob = extract_MB_behavior_data(data_path, id)
    subject_dataframe = pd.DataFrame({
        'repeat': repeat,
        'common_reward': common_rewarded,
        'reward_prob': reward_prob,
        'subject_id': [int(id) for _ in repeat]
    })
    model, result = glmfit(subject_dataframe, formula='repeat ~ common_reward*reward_prob')
    return model, result, subject_dataframe


def extract_MB_behavior_data(data_path, subject_id):

    with open('{}{}/{}-task-phase2.json'.format(data_path, subject_id,subject_id), 'r') as data_file:

        data = json.load(data_file)
        repeat, common_rewarded, reward_probs = [], [], []
        for block in range(TaskParams.n_agent_blocks):
            for i, (pre_trial, trial) in enumerate(zip(
                data[block*TaskParams.n_agent_block_trials:(block+1)*TaskParams.n_agent_block_trials-1],
                data[block*TaskParams.n_agent_block_trials+1:(block+1)*TaskParams.n_agent_block_trials]
            )):
                if find_number_of_common_objects(pre_trial['visited_objects'], trial['possible_objects']) == 1:

                    option_with_common_index = find_option_index_with_common(pre_trial, trial)
                    repeat.append(1 if trial['selected_option'] == trial['options'][option_with_common_index] else 0)

                    common_reward, reward_prob = extract_common_reward_status(
                        pre_trial, trial, option_with_common_index
                    )
                    common_rewarded.append(common_reward)
                    reward_probs.append(reward_prob)

    return repeat, common_rewarded, reward_probs


def find_number_of_common_objects(visited_pair, possible_objects):

    count = 0
    for object in visited_pair:
        if object in possible_objects[0]:
            count += 1
        if object in possible_objects[1]:
            count += 1

    return count


def find_repeat_probs(repeat, common_rewarded):

    calc_prob = lambda values: sum(values)/len(values)

    repeat = np.array(repeat)
    common_rewarded = np.array(common_rewarded)

    common1 = np.where(common_rewarded == 1)
    common1_repeat_prob = calc_prob(repeat[common1])

    common0 = np.where(common_rewarded == 0)
    common0_repeat_prob = calc_prob(repeat[common0])

    return common1_repeat_prob, common0_repeat_prob


def find_option_index_with_common(pre_trial, trial):

    visited_pair = pre_trial['visited_objects']
    for object in visited_pair:
        if object in trial['possible_objects'][0]:
            return 0
        if object in trial['possible_objects'][1]:
            return 1

    return None


def extract_common_reward_status(pre_trial, trial, option_with_common_index):

    objects_set_of_common = trial['possible_objects'][option_with_common_index]
    visited_pair = pre_trial['visited_objects']

    common = None
    for object in objects_set_of_common:
        if object in visited_pair:
            common = object
            break

    selected_option_index = 0
    for i, option in enumerate(pre_trial['options']):
        if option == pre_trial['selected_option']:
            selected_option_index = i
            break

    common_index = 0 if common == visited_pair[0] else 1
    common_reward = int(pre_trial['gained_rewards'][common_index])
    reward_prob = pre_trial['possible_reward_probs'][selected_option_index][common_index]

    return common_reward, reward_prob
