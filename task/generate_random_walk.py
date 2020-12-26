from task.params.task_params import TaskParams
from tools.directory_files import get_file_names

import numpy as np

import copy
import random
import pickle


def set_phase_reward_probs_by_random_walk(prediction_phase=False):

    objects_reward_probs = []
    n_blocks, n_block_trials = \
        (TaskParams.n_agent_blocks, TaskParams.n_agent_block_trials) if prediction_phase \
        else (TaskParams.num_of_blocks, TaskParams.num_of_block_trials)

    for block in range(n_blocks):
        block_rewards, init_probs = [], copy.deepcopy(TaskParams.init_block_probs)
        random.shuffle(init_probs)
        for i in range(n_block_trials):
            block_rewards.append(
                init_probs if i == 0 else _rewards_random_walk(block_rewards[i-1])
            )

        objects_reward_probs.append(block_rewards)

    _save_random_walks(objects_reward_probs)


def _rewards_random_walk(init_probs):

    delta_values = TaskParams.reward_prob_std * np.random.normal(size=np.array(init_probs).shape)
    new_reward_probs = np.array(init_probs) + delta_values

    for i, reward in enumerate(new_reward_probs):
        if reward > TaskParams.max_reward_prob:
            new_reward_probs[i] = TaskParams.max_reward_prob - (reward - TaskParams.max_reward_prob)
        elif reward < TaskParams.min_reward_prob:
            new_reward_probs[i] = TaskParams.min_reward_prob + (TaskParams.min_reward_prob - reward)

    return new_reward_probs.tolist()


def _save_random_walks(generated_random_walk):

    walk_id = 1
    file_names = get_file_names(TaskParams.random_walks_path, 'pkl')
    file_names = [name.replace('walk', '') for name in file_names]
    file_names = [name.replace('.pkl', '') for name in file_names]

    if file_names:
        walk_ids = [int(name) for name in file_names]
        walk_id = max(walk_ids) + 1

    with open('{}walk{}.pkl'.format(TaskParams.random_walks_path, walk_id), 'wb') as file:
        pickle.dump(generated_random_walk, file)





