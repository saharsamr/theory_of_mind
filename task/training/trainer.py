from task.params.task_params import TaskParams
from task.presentation import PresentationClass

import random
from time import sleep


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
    objects_of_quiz_phase2 = []
    options_of_quiz_phase2 = []
    quiz_phase2_responses = []
    quiz_phase2_response_times = []


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
    def set_objects_of_quiz_phase2(cls):

        round_objects = []
        for i in range(cls.num_of_quiz_repeat):
            round_objects.extend(TaskParams.objects)
        random.shuffle(round_objects)

        cls.objects_of_quiz_phase2.append(round_objects)


    @classmethod
    def set_options_of_quiz_phase2(cls, round):

        round_options = []
        for object in cls.objects_of_quiz_phase2[round]:
            selected_options = []
            related_options = [op for op in TaskParams.first_options if object in TaskParams.objects_of_options[op]]
            selected_options.append(random.choice(related_options))
            selected_options.append(
                random.choice([op for op in TaskParams.first_options if op not in related_options])
            )
            random.shuffle(selected_options)
            round_options.append(selected_options)

        cls.options_of_quiz_phase2.append(round_options)


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

            if round_responses[-1] == 1:
                presenter.draw_image(TaskParams.image_dir+'true.png')
            else:
                presenter.draw_image(TaskParams.image_dir+'false.png')

            sleep(TaskParams.feedback_duration)

        cls.quiz_phase1_responses.append(round_responses)
        cls.quiz_phase1_response_times.append(round_response_times)


    @classmethod
    def training_quiz_phase2(cls, presenter, round):

        cls.set_objects_of_quiz_phase2()
        cls.set_options_of_quiz_phase2(round)

        round_responses, round_response_times = [], []
        for object, options in zip(cls.objects_of_quiz_phase2[round], cls.options_of_quiz_phase2[round]):

            key, response_time = presenter.present_quiz_phase2_question(object, options)
            if object in TaskParams.objects_of_options[options[0]]:
                round_responses.append(1 if key == 'left' else 0)
            elif object in TaskParams.objects_of_options[options[1]]:
                round_responses.append(1 if key == 'right' else 0)
            round_response_times.append(response_time)

            if round_responses[-1] == 1:
                presenter.draw_image(TaskParams.image_dir+'true.png')
            else:
                presenter.draw_image(TaskParams.image_dir+'false.png')

            sleep(TaskParams.feedback_duration)

        cls.quiz_phase2_responses.append(round_responses)
        cls.quiz_phase2_response_times.append(round_response_times)


    @classmethod
    def check_quiz_passing(cls):

        last_phase1_responses = cls.quiz_phase1_responses[-1]
        last_phase2_responses = cls.quiz_phase2_responses[-1]
        last_phase1_response_times = cls.quiz_phase1_response_times[-1]
        last_phase2_response_times = cls.quiz_phase2_response_times[-1]

        all_correct, all_fast = True, True
        if 0 in last_phase1_responses or 0 in last_phase2_responses:
            all_correct = False
        if not all(rt <= TaskParams.time_limit_for_quiz for rt in last_phase1_response_times)\
            or not all(rt <= TaskParams.time_limit_for_quiz for rt in last_phase2_response_times):
            all_fast = False

        passed = all_correct and all_fast
        return passed, all_correct, all_fast


    @classmethod
    def start_training(cls, presenter):

        passed, round = False, 0
        while not passed:

            cls.set_training_options_order(round)
            cls.set_objects_presentation_order(round)

            cls.training_presentation_phase(round, presenter)

            presenter.present_instructions('quiz1')
            cls.training_quiz_phase1(presenter, round)

            presenter.present_instructions('quiz2')
            cls.training_quiz_phase2(presenter, round)

            passed, all_correct, all_fast = cls.check_quiz_passing()

            if not all_correct:
                presenter.present_instructions('quiz-mistakes')
            elif not all_fast:
                presenter.present_instructions('quiz-not-fast')
            elif passed:
                presenter.present_instructions('quiz-passed')
