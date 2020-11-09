from task.params.task_params import TaskParams
from task.presentation import PresentationClass

import random


class Trainer:

    num_of_training_repeat = [12, 4, 2]
    training_options_order = []
    objects_presentation_order = []


    @classmethod
    def set_training_options_order(cls, round):

        round_training_order = []
        for i in range(cls.num_of_training_repeat[min(3, round)]):
            round_training_order.extend(TaskParams.first_options)

        random.shuffle(round_training_order)
        cls.training_options_order.append(round_training_order)


    @classmethod
    def set_objects_presentation_order(cls, round):

        round_object_presentation_order = []
        for option in cls.training_options_order[round]:
            objects = TaskParams.objects_of_options[option]
            random.shuffle(objects)
            new_objects = (objects[0], objects[1])
            round_object_presentation_order.append(new_objects)

        cls.objects_presentation_order.append(round_object_presentation_order)


    @classmethod
    def start_training(cls, presenter):

        passed, round = False, 0
        while not passed:
            cls.set_training_options_order(round)
            cls.set_objects_presentation_order(round)
            for option, objects in zip(cls.training_options_order[round], cls.objects_presentation_order[round]):
                presenter.present_training_step(option, objects)
