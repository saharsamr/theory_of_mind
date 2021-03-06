import numpy as np
import pandas as pd


ACCEPTED_CHOICES = [1, 2, 3, 4]
N_BLOCK_TRIALS = 60


def find_common_and_unique_MF(choice, next_trial_options, outcome):

    common = np.intersect1d(outcome[next_trial_options[0]-1], outcome[next_trial_options[1]-1])
    unique = np.setdiff1d(outcome[choice-1], common)
    return common, unique


def find_common_MB(choice, option_with_common, outcome):

    common = np.intersect1d(outcome[choice-1], outcome[option_with_common-1])
    return common


def is_there_just_one_common(choice, next_trial_options, outcome):

    commons_len = [
        len(np.intersect1d(outcome[choice-1], outcome[next_trial_options[0]-1])),
        len(np.intersect1d(outcome[choice-1], outcome[next_trial_options[1]-1]))
    ]
    return np.sum(commons_len) == 1


def find_option_with_common(choice, next_trial_options, outcome):

    if len(np.intersect1d(outcome[choice-1], outcome[next_trial_options[0]-1])):
        return next_trial_options[0]
    elif len(np.intersect1d(outcome[choice-1], outcome[next_trial_options[1]-1])):
        return next_trial_options[1]


def extract_MF_trials_pair_info(\
    model_free_data, choice, next_trial_options, next_choice, outcome, pic_rewards):

    common, unique = find_common_and_unique_MF(choice, next_trial_options, outcome)
    if common:
        model_free_data['common_reward'].append(pic_rewards[common-1][0])
        model_free_data['unique_reward'].append(pic_rewards[unique-1][0])
        model_free_data['repeat'].append(1 if choice == next_choice else 0)

    return model_free_data


def extract_MB_trials_pair_info(\
    model_based_data, choice, next_trial_options, next_choice, outcome, pic_rewards, reward_prob):

    if is_there_just_one_common(choice, next_trial_options, outcome):
        option_with_common = find_option_with_common(choice, next_trial_options, outcome)
        common = find_common_MB(choice, option_with_common, outcome)
        model_based_data['common_reward'].append(pic_rewards[common-1][0])
        model_based_data['repeat'].append(1 if next_choice == option_with_common else 0)
        model_based_data['reward_prob'].append(reward_prob[common-1][0])

    return model_based_data


def extract_subject_trials_info(filtered_data, start_index):

    trials_options = filtered_data['trials']
    chosens = filtered_data['chosen']
    realized_rewards = filtered_data['realized_reward']
    reward_probs = filtered_data['reward_probs']
    outcome = filtered_data['outcome']
    n_trials = len(trials_options)

    model_free_data = {'common_reward': [], 'unique_reward': [], 'repeat': []}
    model_based_data = {'common_reward': [], 'reward_prob': [], 'repeat': []}

    for i, (trial_options, choice, pic_rewards, reward_prob) in \
        enumerate(zip(trials_options, chosens, realized_rewards, reward_probs)):

        next_trial_options = trials_options[(i+1)%n_trials]
        next_choice = chosens[(i+1)%n_trials]

        if (choice in ACCEPTED_CHOICES) and ((i+1+start_index) % N_BLOCK_TRIALS) and (next_choice in ACCEPTED_CHOICES):

            if choice in next_trial_options:
                model_free_data = extract_MF_trials_pair_info(\
                    model_free_data, choice, next_trial_options, next_choice, outcome, pic_rewards)
            else:
                model_based_data = extract_MB_trials_pair_info(\
                    model_based_data, choice, next_trial_options, next_choice, outcome, pic_rewards, reward_prob)

    return pd.DataFrame(model_free_data), pd.DataFrame(model_based_data)


def get_bad_trial_indices(model_based_data):

    new_data = model_based_data
    new_data['reward_prob'] = [int(reward_prob*100/5)*5/100 for reward_prob in model_based_data['reward_prob']]
    groups = new_data.groupby(by=['reward_prob', 'common_reward'])

    indices = []
    for key, group in groups:
        different_states_num = len(np.unique(group['repeat']))
        if different_states_num != 2:
            for index in group.index:
                indices.append(index)

    return indices
