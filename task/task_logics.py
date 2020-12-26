from task.params.task_params import TaskParams
from task.params.subject_params import SubjectParams
from task.trials_info import TrialsInfo

import random
import pickle
import copy
import numpy as np


class TaskLogics:

    @staticmethod
    def assign_trials_pairs():

        task_option_pairs_copy = copy.deepcopy(TaskParams.options_pairs)
        first_four_trials = TaskLogics._find_first_two_pairs(task_option_pairs_copy)
        remained_trials = []

        for i in range(int(TaskParams.n_trials/4)-1):
            remained_trials.extend(task_option_pairs_copy)
        random.shuffle(remained_trials)

        first_four_trials.extend(remained_trials)
        trials_pairs = first_four_trials
        for i in range(len(trials_pairs)):
            same_order = random.choice([0, 1])
            trials_pairs[i] = tuple(trials_pairs[i]) if same_order else (trials_pairs[i][1], trials_pairs[i][0])

        TrialsInfo.set_trials_pairs(
            np.reshape(trials_pairs, (TaskParams.num_of_blocks, TaskParams.num_of_block_trials, 2)).tolist()
        )


    @staticmethod
    def manage_warmup_trials():

        not_finished = lambda sampled, selected: len(sampled) + len(selected) < TaskParams.n_warm_up_trials

        selected_indices = [0, 1, 2, 3]
        random.shuffle(selected_indices)
        sampled_indices, visited_options = [], []
        while not_finished(sampled_indices, selected_indices):
            for ind, trial_pair in enumerate(TrialsInfo.trials_pairs[0]):
                if ind >= len(selected_indices) and not_finished(sampled_indices, selected_indices):
                    if (str(trial_pair) not in visited_options) and (random.random() < 0.1):
                        sampled_indices.append(ind)
                        visited_options.append(str(trial_pair))
                elif not not_finished(sampled_indices, selected_indices):
                    break
        random.shuffle(sampled_indices)

        selected_indices.extend(sampled_indices)
        TrialsInfo.sample_for_warmup(selected_indices)


    @staticmethod
    def set_rewards_for_warmup():

        generated_randoms, actual_rewards = [], []
        for pair_probs in TrialsInfo.warmup_reward_probs:

            pair_random = [(random.random(), random.random()) for _ in pair_probs]
            pair_reward = [(int(rand[0] < prob[0]), int(rand[1] < prob[1])) for rand, prob in zip(pair_random, pair_probs)]
            generated_randoms.append(pair_random)
            actual_rewards.append(pair_reward)

        TrialsInfo.set_rewards_for_warmup(generated_randoms, actual_rewards)


    @staticmethod
    def save_trials_results(selected_keys, reaction_times, predictions=None):

        selected_options, visited_objects, rewards = [], [], []
        for block in range(TaskParams.num_of_blocks):
            block_selected_option, block_visited_objects, block_rewards = \
                TaskLogics.block_trials_results(
                    selected_keys[block],
                    TrialsInfo.trials_pairs[block],
                    TrialsInfo.trials_availables_objects[block],
                    TrialsInfo.available_objects_actual_rewards[block]
                )

            selected_options.append(block_selected_option)
            visited_objects.append(block_visited_objects)
            rewards.append(block_rewards)

        TrialsInfo.set_subjects_selection(selected_options)
        TrialsInfo.set_visited_objects(visited_objects)
        TrialsInfo.set_gained_rewards(rewards)
        TrialsInfo.set_selection_reaction_times(reaction_times)


    @staticmethod
    def save_agent_trials_results(selected_options, visited_objects, gained_rewards, predictions, reaction_times):

        TrialsInfo.set_subjects_selection(selected_options)
        TrialsInfo.set_visited_objects(visited_objects)
        TrialsInfo.set_gained_rewards(gained_rewards)
        TrialsInfo.set_subject_predictions(predictions)
        TrialsInfo.set_selection_reaction_times(reaction_times)


    @staticmethod
    def save_warmup_results(selected_keys, reaction_times):

        selected_options, visited_objects, rewards = \
            TaskLogics.block_trials_results(
                selected_keys,
                TrialsInfo.warmup_trials_pairs,
                TrialsInfo.warmup_available_objects,
                TrialsInfo.warmup_objects_actual_rewards
            )

        TrialsInfo.set_warmup_selections(selected_options)
        TrialsInfo.set_warmup_visited_objects(visited_objects)
        TrialsInfo.set_warmup_gained_rewards(rewards)
        TrialsInfo.set_warmup_reaction_times(reaction_times)


    @staticmethod
    def block_trials_results(selected_keys, trials_pairs, trials_objects, trials_rewards):

        block_selected_option, block_visited_objects, block_rewards = [], [], []
        for t_index, key in enumerate(selected_keys):

            if key:
                option_index = 0 if key == 'left' else 1
                selected_option = trials_pairs[t_index][option_index]
                block_selected_option.append(selected_option)
                block_visited_objects.append(trials_objects[t_index][option_index])
                block_rewards.append(trials_rewards[t_index][option_index])
            else:
                block_selected_option.append(None)
                block_visited_objects.append(None)
                block_rewards.append(None)

        return block_selected_option, block_visited_objects, block_rewards


    @staticmethod
    def set_available_objects_in_trials():

        objects = []
        for block in range(TaskParams.num_of_blocks):
            block_objects = []
            for pair in TrialsInfo.trials_pairs[block]:

                objects1 = TaskParams.objects_of_options[pair[0]]
                objects2 = TaskParams.objects_of_options[pair[1]]
                random.shuffle(objects1), random.shuffle(objects2)
                trial_objects = [objects1, objects2]
                block_objects.append(trial_objects)

            objects.append(block_objects)

        TrialsInfo.set_trials_available_objects(objects)


    @staticmethod
    def set_objects_reward_probs(phase):

        random_walk_file_name = '{}walk{}.pkl'.format(
            TaskParams.random_walks_path, SubjectParams.phases_random_walks[phase-1]
        )
        with open(random_walk_file_name, 'rb') as file:
            objects_reward_probs = pickle.load(file)

        TrialsInfo.set_objects_reward_probs(objects_reward_probs)


    @staticmethod
    def store_trials_available_objects_reward_prob():

        all_trials_probs = []
        for block in range(TaskParams.num_of_blocks):
            block_trials_reward_probs = []
            for trial_objects, objects_reward_probs in zip(\
                TrialsInfo.trials_availables_objects[block], TrialsInfo.objects_reward_probs_during_trials[block]\
            ):
                objects1, objects2 = trial_objects
                trial_rewards_probs = [
                    (objects_reward_probs[objects1[0]%10], objects_reward_probs[objects1[1]%10]),
                    (objects_reward_probs[objects2[0]%10], objects_reward_probs[objects2[1]%10])
                ]
                block_trials_reward_probs.append(trial_rewards_probs)
            all_trials_probs.append(block_trials_reward_probs)

        TrialsInfo.set_available_objects_reward_probs(all_trials_probs)


    @staticmethod
    def set_objects_actual_rewards():

        generated_randoms, actual_rewards = [], []
        for block in range(TaskParams.num_of_blocks):
            block_randoms, block_rewards = [], []
            for objects_rewards_probs in TrialsInfo.trials_availables_objects_reward_probs[block]:
                temp_radoms, temp_rewards = [], []
                for object_set in objects_rewards_probs:
                    randoms = (random.random(), random.random())
                    rewards = (randoms[0] < object_set[0], randoms[1] < object_set[1])
                    temp_radoms.append(randoms)
                    temp_rewards.append(rewards)

                block_randoms.append(temp_radoms)
                block_rewards.append(temp_rewards)

            generated_randoms.append(block_randoms)
            actual_rewards.append(block_rewards)

        TrialsInfo.set_generated_randoms_for_rewards(generated_randoms)
        TrialsInfo.set_objects_actual_rewards(actual_rewards)


    @staticmethod
    def _find_first_two_pairs(task_option_pairs_copy):

        selected_pairs = [task_option_pairs_copy[0]]
        for pair in task_option_pairs_copy:
            if pair[0] not in selected_pairs[0] and pair[1] not in selected_pairs[0]:
                selected_pairs.append(pair)

        for pair in task_option_pairs_copy:
            if pair not in selected_pairs:
                selected_pairs.append(pair)

        return selected_pairs


    @staticmethod
    def assign_objects_to_options():

        objects_of_options = [[], [], [], []]
        objects_temp = [ob for ob in TaskParams.objects]
        random.shuffle(objects_temp)

        for i, (object, pair) in enumerate(zip(objects_temp, TaskParams.options_pairs)):
            for option in pair:
                objects_of_options[option].append(object)

        TaskParams.set_objects_of_options(objects_of_options)


    @staticmethod
    def pair_options():

        first_options = [op for op in TaskParams.first_options]
        second_options = [op for op in TaskParams.second_options]
        pairs, pairs_num = [], len(first_options)

        for i in range(pairs_num):

            first = random.choice(first_options)
            second_options_temp = [op for op in second_options if (op != first) and ([op, first] not in pairs)]
            second = random.choice(second_options_temp)

            if i == pairs_num - 2:
                if not TaskLogics._all_options_came_in_first_three(
                    pairs, [first, second], TaskParams.first_options
                ):
                    second = [op for op in second_options_temp if second != op][0]

            first_options.remove(first)
            second_options.remove(second)
            pairs.append([first, second])

        TaskParams.set_options_pairs(pairs)


    @staticmethod
    def _all_options_came_in_first_three(previous_pairs, new_pair, all_options):

        temp_pairs = previous_pairs
        temp_pairs.append(new_pair)

        for option in all_options:
            selected = False
            for pair in temp_pairs:
                for selected_option in pair:
                    if option == selected_option:
                        selected = True

            if not selected:
                temp_pairs.remove(new_pair)
                return False

        temp_pairs.remove(new_pair)
        return True
