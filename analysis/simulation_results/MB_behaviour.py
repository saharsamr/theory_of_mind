from task.params.task_params import TaskParams
from analysis.simulation_results.tools import find_common_unique_object

import numpy as np

import json


def extract_MB_behavior_data(data_path, subject_id):

    with open('{}{}/{}-task-phase2.json'.format(data_path, subject_id,subject_id), 'r') as data_file:

        data = json.load(data_file)
        repeat, common_rewarded = [], []
        for block in range(TaskParams.n_agent_blocks):
            for i, (pre_trial, trial) in enumerate(zip(
                data[block*TaskParams.n_agent_block_trials:(block+1)*TaskParams.n_agent_block_trials-1],
                data[block*TaskParams.n_agent_block_trials+1:(block+1)*TaskParams.n_agent_block_trials]
            )):
                if find_number_of_common_objects(pre_trial['visited_objects'], trial['possible_objects']) == 1:

                    option_with_common_index = find_option_index_with_common(pre_trial, trial)
                    repeat.append(1 if trial['selected_option'] == trial['options'][option_with_common_index] else 0)

                    common_reward = extract_common_reward_status(pre_trial, trial, option_with_common_index)
                    common_rewarded.append(common_reward)

    return find_repeat_probs(repeat, common_rewarded)



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

    common, unique = find_common_unique_object(visited_pair, objects_set_of_common)

    common_index = 0 if common == visited_pair[0] else 1
    common_reward = int(pre_trial['gained_rewards'][common_index])

    return common_reward
