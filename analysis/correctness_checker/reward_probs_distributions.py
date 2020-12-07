from task.params.task_params import TaskParams

import matplotlib.pyplot as plt
import numpy as np

import json


def plot_rewards_probs_distr(data_path, subject_id):

    probs = extract_reward_probs(data_path, subject_id, 'task-phase1')

    xs = [x for x in range(len(probs[0]))]
    plt.plot(xs, probs[0], label='p0')
    plt.plot(xs, probs[1], label='p1')
    plt.plot(xs, probs[2], label='p2')
    plt.plot(xs, probs[3], label='p3')
    plt.legend()
    plt.show()


def extract_reward_probs(data_path, subject_id, phase_name):

    with open('{}{}/{}-{}.json'.format(data_path, subject_id,subject_id, phase_name), 'r') as data_file:

        data = json.load(data_file)
        reward_probs = []
        for trial in data:
            reward_probs.append(trial['all_reward_probs'])

    return np.array(reward_probs).transpose()
