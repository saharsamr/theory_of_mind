from task.params.task_params import TaskParams
from task.trials_info import TrialsInfo

import random
import copy
import numpy as np
from collections import defaultdict


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

        TrialsInfo.set_trials_pairs(np.reshape(trials_pairs, (5, 60, 2)))


    @staticmethod
    def set_available_objects_in_trials():

        objects = []
        for block in range(TaskParams.num_of_blocks):
            block_objects = []
            for pair in TrialsInfo.trials_pairs[block]:

                objects1 = TaskParams.objects_of_options[pair[0]]
                objects2 = TaskParams.objects_of_options[pair[1]]
                random.shuffle(objects1), random.shuffle(objects2)
                trial_objects = [tuple(objects1), tuple(objects2)]
                block_objects.append(trial_objects)

            objects.append(block_objects)

        TrialsInfo.set_trials_available_objects(objects)


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
