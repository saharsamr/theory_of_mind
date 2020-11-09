from task.params.task_params import TaskParams

import random


class Trainer:

    num_of_training_repeat = [12, 4, 2]
    training_options_order = []


    @classmethod
    def set_training_options_order(cls, round):

        round_training_order = []
        for i in range(cls.num_of_training_repeat[min(3, round)]):
            round_training_order.extend(TaskParams.first_options)

        random.shuffle(round_training_order)
        print(round_training_order)
        cls.training_options_order.append(round_training_order)
