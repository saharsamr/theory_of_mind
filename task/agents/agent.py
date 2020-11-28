from task.params.task_params import TaskParams
from task.task_logics import TaskLogics
from task.trials_info import TrialsInfo
from task.task import Task

import numpy as np
import random

import abc


class Agent(abc.ABC):

    option_qvalues = {}
    lr_param = 0.05
    forgetting_param = 0.05
    softmax_param = 0.09


    @classmethod
    def initialize_trials(cls):

        cls.initialize_qvalues()

        TaskLogics.assign_trials_pairs()
        TaskLogics.set_available_objects_in_trials()
        TaskLogics.set_objects_reward_probs_by_random_walk()
        TaskLogics.store_trials_available_objects_reward_prob()
        TaskLogics.set_objects_actual_rewards()


    @classmethod
    @abc.abstractclassmethod
    def initialize_qvalues(cls):
        pass


    @classmethod
    @abc.abstractclassmethod
    def update_qvalues(cls, option, objects, rewards):
        pass


    @classmethod
    def start_agent_task(cls):

        selecteds, reaction_times = [], []
        for block in range(TaskParams.n_agent_blocks):

            block_selected, block_reaction_time, block_rewards, block_objects = \
            cls.run_agent_trials_block(
                TaskParams.n_agent_block_trials,
                TrialsInfo.trials_pairs[block],
                TrialsInfo.trials_availables_objects[block],
                TrialsInfo.available_objects_actual_rewards[block],
                TaskParams.time_limit_for_selection,
            )

            selecteds.append(block_selected)
            reaction_times.append(block_reaction_time)

        TaskLogics.save_tirals_results(selecteds, reaction_times)


    @classmethod
    def run_agent_trials_block(
        cls, num_block_trials, block_trial_pairs, block_available_objects,
        block_object_rewards, time_limit=float('inf')
    ):

        block_selected, block_reaction_time, block_rewards, block_objects = [], [], [], []
        for t_index in range(num_block_trials):

            selected, reaction_time = cls.select_option(block_trial_pairs[t_index])

            selected_index = np.where(block_trial_pairs[t_index] == selected)[0][0]
            rewards = block_object_rewards[t_index][selected_index]
            objects = block_available_objects[t_index][selected_index]

            cls.update_qvalues(selected, objects, rewards)

            block_selected.append(selected)
            block_reaction_time.append(reaction_time)
            block_rewards.append(rewards)
            block_objects.append(objects)

        return block_selected, block_reaction_time, block_rewards, block_objects


    @classmethod
    def select_option(cls, options):

        all_options_qvalues = np.array([cls.option_qvalues[option] for option in options])
        options_probs = [Agent.softmax(cls.option_qvalues[option], all_options_qvalues) for option in options]
        selected = np.random.choice(options, p=options_probs)

        reaction_time = max(
            random.random() * TaskParams.time_limit_for_selection,
            TaskParams.min_time_for_agent_slection
        )

        return selected, reaction_time


    @classmethod
    def softmax(cls, option_q, all_q):

        numerator = np.exp(cls.softmax_param*option_q)
        denominator = sum(np.exp(cls.softmax_param*all_q))

        return numerator/denominator
