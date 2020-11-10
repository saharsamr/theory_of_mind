from task.params.task_params import TaskParams
from task.presentation import PresentationClass

import random


class Trainer:

    num_of_training_repeat = [12, 4, 2]
    training_options_order = []
    objects_presentation_order = []
    presentation_response_times = []
    
    num_of_quiz_repeat = 2
    objects_of_quiz_phase1 = []
    options_of_quiz_phase1 = []
    quiz_phase1_responses = []
    quiz_phase1_response_times = []


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
    def set_options_of_quiz_phase1(cls):

        round_options = []
        for i in range(cls.num_of_quiz_repeat):
            round_options.extend(TaskParams.first_options)
        random.shuffle(round_options)

        cls.options_of_quiz_phase1.append(round_options)


    @classmethod
    def set_objects_of_quiz_phase1(cls, round):

        round_objects = []
        for option in cls.options_of_quiz_phase1[round]:
            selected_objects = []
            objects = TaskParams.objects_of_options[option]
            selected_objects.append(random.choice(objects))
            selected_objects.append(
                random.choice([ob for ob in TaskParams.objects if ob not in objects])
            )
            random.shuffle(selected_objects)
            round_objects.append(selected_objects)

        cls.objects_of_quiz_phase1.append(round_objects)


    @classmethod
    def training_presentation_phase(cls, round, presenter):

        round_presentation_response_times = []
        for option, objects in zip(cls.training_options_order[round], cls.objects_presentation_order[round]):
            reaction_time = presenter.present_training_step(option, objects)
            round_presentation_response_times.append(reaction_time)

        cls.presentation_response_times.append(round_presentation_response_times)


    @classmethod
    def training_quiz_phase1(cls, presenter, round):

        cls.set_options_of_quiz_phase1()
        cls.set_objects_of_quiz_phase1(round)

        round_responses, round_response_times = [], []
        for option, objects in zip(cls.options_of_quiz_phase1[round], cls.objects_of_quiz_phase1[round]):

            key, response_time = presenter.present_quiz_phase1_question(option, objects)
            if objects[0] in TaskParams.objects_of_options[option]:
                round_responses.append(1 if key == 'left' else 0)
            elif objects[1] in TaskParams.objects_of_options[option]:
                round_responses.append(1 if key == 'right' else 0)
            round_response_times.append(response_time)

        cls.quiz_phase1_responses.append(round_responses)
        cls.quiz_phase1_response_times.append(round_response_times)


    @classmethod
    def start_training(cls, presenter):

        passed, round = False, 0
        while not passed:
            cls.set_training_options_order(round)
            cls.set_objects_presentation_order(round)
            cls.training_presentation_phase(round, presenter)
            cls.training_quiz_phase1(presenter, round)
