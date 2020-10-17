import numpy as np
import pandas as pd


ACCEPTED_CHOICES = [1, 2, 3, 4]
N_TRIALS = 300
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



def extract_MB_MF_info(trails_options, chosens, realized_rewards, reward_probs, outcome):

    common_reward_MF, unique_reward_MF = [], []
    repeat_MF = []
    common_reward_MB = []
    repeat_MB, reward_prob_MB = [], []

    for i, (trial_options, choice, pic_rewards, reward_prob) in \
        enumerate(zip(trails_options, chosens, realized_rewards, reward_probs)):

        next_trial_options = trails_options[(i+1)%N_TRIALS]
        next_choice = chosens[(i+1)%N_TRIALS]

        if (choice in ACCEPTED_CHOICES) and ((i+1) % N_BLOCK_TRIALS) and (next_choice in ACCEPTED_CHOICES):

            if choice in next_trial_options:
                common, unique = find_common_and_unique_MF(choice, next_trial_options, outcome)
                if common:
                    common_reward_MF.append(pic_rewards[common-1][0])
                    unique_reward_MF.append(pic_rewards[unique-1][0])
                    repeat_MF.append(choice == next_choice)

            else:
                if is_there_just_one_common(choice, next_trial_options, outcome):
                    option_with_common = find_option_with_common(choice, next_trial_options, outcome)
                    common = find_common_MB(choice, option_with_common, outcome)
                    common_reward_MB.append(pic_rewards[common-1][0])
                    repeat_MB.append(next_choice == option_with_common)
                    reward_prob_MB.append(reward_prob[common-1][0])

    return np.array(common_reward_MF), np.array(unique_reward_MF), np.array(repeat_MF),\
            np.array(common_reward_MB), np.array(repeat_MB), np.array(reward_prob_MB)
