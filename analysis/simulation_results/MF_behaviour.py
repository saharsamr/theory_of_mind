from task.params.task_params import TaskParams
from analysis.simulation_results.tools import find_common_unique_object

import numpy as np

import json


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

                    print(pre_trial['agent'])
                    print(pre_trial['possible_objects'])
                    print(pre_trial['visited_objects'])
                    print(pre_trial['possible_actual_rewards'])
                    print(pre_trial['gained_rewards'])

                    repeat.append(1 if pre_trial['selected_option'] == trial['selected_option'] else 0)

                    common_reward, unique_reward = extract_common_unique_reward_status(pre_trial)
                    common_rewarded.append(common_reward)
                    unique_rewarded.append(unique_reward)

                    print(common_reward)
                    print(unique_reward)
                    print('-----------------------------------------')

    return find_repeat_probs(repeat, common_rewarded, unique_rewarded)


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


def extract_common_unique_reward_status(pre_trial):

    difference = lambda pair, object: pair[0] if object != pair[0] else pair[1]

    visited_pair = pre_trial['visited_objects']
    other_pair = difference(pre_trial['possible_objects'], visited_pair)

    common, unique = find_common_unique_object(visited_pair, other_pair)

    common_index = 0 if common == visited_pair[0] else 1
    common_reward = int(pre_trial['gained_rewards'][common_index])
    unique_reward = int(pre_trial['gained_rewards'][1-common_index])

    return common_reward, unique_reward
