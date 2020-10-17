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
                    print(pic_rewards[common-1][0])
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


def groupby_data_single_subject_MF(common_reward_MF, unique_reward_MF, repeat_MF):

    data = np.empty((4, 4))
    for i, common_reward in enumerate([0, 1]):
        for j, unique_reward in enumerate([0, 1]):

            data[i*2+j][0] = common_reward
            data[i*2+j][1] = unique_reward
            data[i*2+j][2] = len(np.where(\
                (common_reward_MF == common_reward) & (unique_reward_MF == unique_reward) & (repeat_MF == True))[0]\
            )
            data[i*2+j][3] = len(np.where(\
                (common_reward_MF == common_reward) & (unique_reward_MF == unique_reward) & (repeat_MF == False))[0]\
            )

    return pd.DataFrame(data, columns=['common_reward', 'unique_reward', 'repeat', 'not_repeat'])


def groupby_data_single_subject_MB(common_reward_MB, reward_prob_MB, repeat_MB):

    unique_reward_probs = np.unique(reward_prob_MB)
    data = np.empty((2*len(unique_reward_probs), 4))
    for i, common_reward in enumerate([0, 1]):
        for j, reward_prob in enumerate(unique_reward_probs):

            data[i*2+j][0] = common_reward
            data[i*2+j][1] = reward_prob
            data[i*2+j][2] = len(np.where(\
                (common_reward_MB == common_reward) & (reward_prob_MB == reward_prob) & (repeat_MB == True))[0]\
            )
            data[i*2+j][2] = len(np.where(\
                (common_reward_MB == common_reward) & (reward_prob_MB == reward_prob) & (repeat_MB == False))[0]\
            )

    return pd.DataFrame(data, columns=['common_reward', 'reward_prob', 'repeat', 'not_repeat'])


def calc_repeat_probs_MF(common_reward_MF, unique_reward_MF, repeat_MF):

    common_1_unique_1_indices = np.where(common_reward_MF == 1 and unique_reward_MF == 1)
    common_1_unique_0_indices = np.where(common_reward_MF == 1 and unique_reward_MF == 0)
    common_0_unique_1_indices = np.where(common_reward_MF == 0 and unique_reward_MF == 1)
    common_0_unique_0_indices = np.where(common_reward_MF == 0 and unique_reward_MF == 0)

    return {
        'common_1_unique_1': np.mean(repeat_MF[common_1_unique_1_indices]),
        'common_1_unique_0': np.mean(repeat_MF[common_1_unique_0_indices]),
        'common_0_unique_1': np.mean(repeat_MF[common_0_unique_1_indices]),
        'common_0_unique_0': np.mean(repeat_MF[common_0_unique_0_indices])
    }


def calc_repeat_probs_MB(common_reward_MB, repeat_MB):

    common_1_indices = np.where(common_reward_MB == 1)
    common_0_indices = np.where(common_reward_MB == 0)

    return {
        'common_1': np.mean(repeat_MB[common_1_indices]),
        'common_0': np.mean(repeat_MB[common_0_indices])
    }
