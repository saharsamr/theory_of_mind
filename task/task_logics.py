from task.params.task_params import TaskParams

import random


class TaskLogics:

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
