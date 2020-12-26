from task.params.task_params import TaskParams
from task.task_logics import TaskLogics
from task.trials_info import TrialsInfo

import numpy as np

import abc


class Agent(abc.ABC):

    option_qvalues = {}
    lr_param = 0.5
    forgetting_param = 0.05
    softmax_param = 1.0


    @classmethod
    def initialize_trials(cls, phase=2):

        cls.initialize_qvalues()

        TrialsInfo.reinitialize_trials_info()
        TaskLogics.assign_trials_pairs()
        TaskLogics.set_available_objects_in_trials()
        TaskLogics.set_objects_reward_probs(phase)
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
    def start_agent_task(cls, presenter):

        selecteds, visited_objects, rewards = [], [], []
        reaction_times, predicteds = [], []
        for block in range(TaskParams.n_agent_blocks):

            cls.initialize_qvalues()
            block_selected, block_rewards, block_objects, block_reaction_time, block_predicted = \
            cls.run_agent_trials_block(
                presenter,
                TaskParams.n_agent_block_trials,
                TrialsInfo.trials_pairs[block],
                TrialsInfo.trials_availables_objects[block],
                TrialsInfo.available_objects_actual_rewards[block],
            )

            selecteds.append(block_selected)
            visited_objects.append(block_objects)
            rewards.append(block_rewards)
            reaction_times.append(block_reaction_time)
            predicteds.append(block_predicted)

        TaskLogics.save_agent_trials_results(selecteds, visited_objects, rewards, predicteds, reaction_times)


    @classmethod
    def run_agent_trials_block(
        cls, presenter, num_block_trials, block_trial_pairs,
        block_available_objects, block_object_rewards, time_limit=float('inf')
    ):

        block_selected, block_rewards, block_objects = [], [], []
        block_reaction_time, block_predicted = [], []
        for t_index in range(num_block_trials):

            selected = cls.select_option(block_trial_pairs[t_index])

            selected_index = np.where(block_trial_pairs[t_index] == selected)[0][0]
            rewards = block_object_rewards[t_index][selected_index]
            objects = block_available_objects[t_index][selected_index]

            key, reaction_time = presenter.present_agent_trial(block_trial_pairs[t_index], selected, objects, rewards)
            predicted = block_trial_pairs[t_index][0] if key == 'left' else block_trial_pairs[t_index][1]

            cls.update_qvalues(selected, objects, rewards)

            block_selected.append(selected.item())
            block_rewards.append(rewards)
            block_objects.append(objects)
            block_reaction_time.append(reaction_time)
            block_predicted.append(predicted)

        return block_selected, block_rewards, block_objects, block_reaction_time, block_predicted


    @classmethod
    def select_option(cls, options):

        all_options_qvalues = np.array([cls.option_qvalues[option] for option in options])
        options_probs = [Agent.softmax(cls.option_qvalues[option], all_options_qvalues) for option in options]
        selected = np.random.choice(options, p=options_probs)

        return selected


    @classmethod
    def softmax(cls, option_q, all_q):

        numerator = np.exp(cls.softmax_param*option_q)
        denominator = sum(np.exp(cls.softmax_param*all_q))

        return numerator/denominator
