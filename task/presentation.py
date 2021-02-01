from task.params.task_params import TaskParams
from task.params.scr_params import SCRParams
from tools.directory_files import get_file_names
from task.interactions import Interaction

from psychopy import visual, core, gui, event

from time import sleep, time


class PresentationClass:

    def __init__(self, screen_size):
        self.screen = visual.Window(screen_size, monitor="testMonitor", units="pix", fullscr=True)


    def present_info_box(self):

        self.exit_fullscreen()

        dlg = gui.Dlg(title="Subject's Info")
        dlg.addField('Name:')
        dlg.addField('Age:')
        dlg.addField('Gender:', choices=['Male', 'Female', 'Other'])
        ok_data = dlg.show()

        self.enter_fullscreen()

        if dlg.OK:
            return {'name': ok_data[0], 'age': ok_data[1], 'gender': ok_data[2]}
        return None


    def exit_fullscreen(self):

        self.screen.fullscr = False
        self.screen.winHandle.set_fullscreen(False)
        self.screen.winHandle.minimize()
        self.screen.flip()


    def enter_fullscreen(self):

        self.screen.winHandle.maximize()
        self.screen.winHandle.activate()
        self.screen.fullscr = True
        self.screen.winHandle.set_fullscreen(True)
        self.screen.flip()


    def convert_relative_to_absolute_pos_size(self, poses, sizes):

        scr_size = SCRParams.screen_size

        real_pos = [
            int(poses[0] * scr_size[0]), int(poses[1] * scr_size[1])
        ]
        real_size = None if sizes == None else [
            int(scr_size[0] * sizes[0]), int(scr_size[1] * sizes[1])
        ]

        return real_pos, real_size

    def draw_image(self, image_path, pos=[0, 0], size=None, flip=True):

        real_pos, real_size = self.convert_relative_to_absolute_pos_size(pos, size)
        image = visual.ImageStim(self.screen, image_path, pos=real_pos, size=real_size)
        image.draw()
        if flip:
            self.screen.flip()


    def draw_multiple_images(self, images_path, poses, sizes, flip=True):

        for path, pos, size in zip(images_path, poses, sizes):
            real_pos, real_size = self.convert_relative_to_absolute_pos_size(pos, size)
            image = visual.ImageStim(self.screen, path, pos=real_pos, size=real_size)
            image.draw()
        if flip:
            self.screen.flip()


    def present_rest(self):

        self.draw_image(TaskParams.image_dir + 'rest.png', size=SCRParams.screen_size)
        sleep(TaskParams.time_for_rest)


    def draw_rectangle(self, x1, y1, x2, y2, color):

        self.draw_line(x1, y1, x2, y1, color)
        self.draw_line(x1, y2, x2, y2, color)
        self.draw_line(x1, y1, x1, y2, color)
        self.draw_line(x2, y1, x2, y2, color)


    def draw_line(self, x1, y1, x2, y2, color):

        line = visual.Line(self.screen)
        line.start, line.end = [x1, y1], [x2, y2]
        line.setColor(color, 'rgb')
        line.lineWidth = 5
        line.draw()


    def draw_trial_options(self, options, flip=True):

        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, options[0]), '{}{}.jpg'.format(TaskParams.image_dir, options[1])],
            [
                [-SCRParams.option_x_index, SCRParams.option_y_index],
                [SCRParams.option_x_index, SCRParams.option_y_index]
            ],
            [
                [SCRParams.option_x_size, SCRParams.option_y_size],
                [SCRParams.option_x_size, SCRParams.option_y_size]
            ], flip=flip
        )

    def present_trial(self, options, objects, rewards, time_limit=float('inf')):

        start, reaction_time = time(), 0
        self.draw_trial_options(options)

        key = Interaction.option_select(time_limit)
        if not key:
            self.draw_image(
                TaskParams.image_dir+'faster.png',
                size=[SCRParams.alerts_x_size, SCRParams.alerts_y_size]
            )
            sleep(TaskParams.feedback_duration)
            return key, float('inf')
        reaction_time = time() - start

        index = 0 if key == 'left' else 1
        self.draw_trial_options(options, flip=False)
        self.draw_selected_rectangle(key)
        self.screen.flip()
        sleep(TaskParams.lag_to_response)

        self.present_objects_rewards(options[index], objects[index], rewards[index])

        return key, reaction_time


    def draw_selected_rectangle(self, key, color=[-1, 1, -1]):

        scr_size = SCRParams.screen_size
        if key == 'left':
            x1, x2 = int(SCRParams.l_rect_left*scr_size[0]), int(SCRParams.l_rect_right*scr_size[0])
        elif key == 'right':
            x1, x2 = int(SCRParams.r_rect_left*scr_size[0]), int(SCRParams.r_rect_right*scr_size[0])

        y1, y2 = int(SCRParams.rect_top*scr_size[1]), int(SCRParams.rect_buttom*scr_size[1])

        self.draw_rectangle(x1, y1, x2, y2, color)


    def present_agent_trial(self, options, selected, selected_objects, selected_rewards, time_limit=float('inf')):

        start, reaction_time = time(), 0
        self.draw_trial_options(options)
        key = Interaction.option_select(time_limit)

        reaction_time = time() - start

        self.present_objects_rewards(selected, selected_objects, selected_rewards)

        predicted_option = options[0] if key == 'left' else options[1]
        self.screen.flip()
        sleep(TaskParams.lag_to_response)
        self.present_prediction_reward(predicted_option, selected)

        return key, reaction_time


    def present_prediction_training_step(self, options, selected, predicted, time_limit=float('inf')):

        agent_selected = self.ask_question_find_answer(
            '{}agent_selection?.png'.format(TaskParams.image_dir),
            options, selected, time_limit
        )

        user_predicted = self.ask_question_find_answer(
            '{}user_prediction?.png'.format(TaskParams.image_dir),
            options, predicted, time_limit
        )

        return agent_selected, user_predicted


    def ask_question_find_answer(self, question_image, options, selected, time_limit):

        self.draw_image(
            question_image,
            size=[SCRParams.instruction_x_size, SCRParams.instruction_y_size]
        )
        sleep(TaskParams.time_limit_training_question)
        agent_selected = \
            self.present_prediction_training_question(options, selected, time_limit)
        sleep(TaskParams.feedback_duration)

        return agent_selected


    def present_prediction_training_question(self, options, true_response, time_limit=float('inf')):

        self.draw_trial_options(options)
        key = Interaction.option_select(time_limit)
        response_index = 0 if key == 'left' else 1

        if true_response == options[response_index]:
            self.draw_image(TaskParams.image_dir + 'true.png')
        else:
            self.draw_image(TaskParams.image_dir + 'false.png')

        return options[response_index]


    def present_prediction_reward(self, predicted_option, selected_option):

        if predicted_option != selected_option:
            self.draw_image(
                TaskParams.image_dir+'fail.png',
                size=[SCRParams.prediction_reward_x_size, SCRParams.prediction_reward_y_size]
            )
        else:
            self.draw_multiple_images(
                [TaskParams.image_dir+'check.png', TaskParams.image_dir+'money.png'],
                [
                    [SCRParams.prediction_reward_x_index, SCRParams.prediction_reward_y_index],
                    [SCRParams.money_x_index, SCRParams.money_y_index]
                ],
                [
                    [SCRParams.prediction_reward_x_size, SCRParams.prediction_reward_y_size],
                    [SCRParams.money_x_size, SCRParams.money_y_size]
                ]
            )
        sleep(TaskParams.feedback_duration)


    def present_objects_rewards(self, option, objects, rewards):

        self.draw_image('{}gray.png'.format(TaskParams.image_dir))
        sleep(TaskParams.lag_to_response)
        for i, (object, reward) in enumerate(zip(objects, rewards)):
            self.draw_multiple_images(
                [
                    '{}{}.jpg'.format(TaskParams.image_dir, option),
                    '{}{}.jpg'.format(TaskParams.image_dir, object),
                    '{}{}.png'.format(TaskParams.image_dir, 'reward' if reward else 'box')
                ],
                [
                    [SCRParams.small_option_x_index, SCRParams.small_option_y_index],
                    [SCRParams.object_x_index, SCRParams.object_y_index],
                    [SCRParams.reward_x_index, SCRParams.reward_y_index]
                ],
                [
                    [SCRParams.small_option_x_size, SCRParams.small_option_y_size],
                    [SCRParams.object_x_size, SCRParams.object_y_size],
                    [SCRParams.reward_x_size, SCRParams.reward_y_size]
                ]
            )
            sleep(TaskParams.feedback_duration)

            if i == 0:
                self.draw_image('{}gray.png'.format(TaskParams.image_dir), flip=False)
                self.draw_image(
                    '{}{}.jpg'.format(TaskParams.image_dir, option),
                    size=[SCRParams.small_option_x_size, SCRParams.small_option_y_size],
                    pos=[SCRParams.small_option_x_index, SCRParams.small_option_y_index]
                )
            else:
                self.draw_image('{}gray.png'.format(TaskParams.image_dir))

            sleep(TaskParams.clear_after_feedback)


    def present_instructions(self, related_phase):

        instruction_folder = TaskParams.instructions_path + related_phase + '/'
        images_name = sorted(get_file_names(instruction_folder, extention='png'))

        instruction_index, num_of_images = 0, len(images_name)
        while True:

            image = images_name[instruction_index]
            self.draw_image(
                instruction_folder+image,
                size=[SCRParams.instruction_x_size, SCRParams.instruction_y_size]
            )

            key_list = Interaction.instrutions_allowed_keys(instruction_index, num_of_images)
            keys = event.waitKeys(keyList=key_list)

            instruction_index += 1 if keys[0] == 'left' else -1

            if keys[0] == 'space':
                break


    def draw_option_object_training(self, object, option):

        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, object), '{}{}.jpg'.format(TaskParams.image_dir, option)],
            [
                [SCRParams.training_object_x_index, SCRParams.training_object_y_index],
                [SCRParams.training_option_x_index, SCRParams.training_option_y_index]
            ],
            [
                [SCRParams.training_object_x_size, SCRParams.training_object_y_size],
                [SCRParams.option_x_size, SCRParams.option_y_size]]
        )


    def present_training_step(self, option, objects):

        start, reaction_time = time(), 0
        self.draw_image(
            TaskParams.image_dir+str(option)+'.jpg',
            pos=[SCRParams.training_option_x_index, SCRParams.training_option_y_index],
            size=[SCRParams.option_x_size, SCRParams.option_y_size]
        )
        if Interaction.ready_to_present_option_objects():
            reaction_time = time() - start
            sleep(TaskParams.lag_to_response)

        self.draw_option_object_training(objects[0], option)
        sleep(TaskParams.object_presentation_time_in_training)


        self.draw_option_object_training(objects[1], option)
        sleep(TaskParams.object_presentation_time_in_training)

        self.draw_image(TaskParams.image_dir+'gray.png')
        sleep(0.25)

        return reaction_time


    def present_quiz_phase1_question(self, option, objects):

        start, reaction_time = time(), 0
        self.draw_multiple_images(
            [
                '{}{}.jpg'.format(TaskParams.image_dir, option),
                '{}{}.jpg'.format(TaskParams.image_dir, objects[0]),
                '{}{}.jpg'.format(TaskParams.image_dir, objects[1])
            ],
            [
                [SCRParams.quiz1_option_x_index, SCRParams.quiz1_option_y_index],
                [-SCRParams.quiz1_object_x_index, SCRParams.quiz1_object_y_index],
                [SCRParams.quiz1_object_x_index, SCRParams.quiz1_object_y_index]
            ],
            [
                [SCRParams.option_x_size, SCRParams.option_y_size],
                [SCRParams.training_object_x_size, SCRParams.training_object_y_size],
                [SCRParams.training_object_x_size, SCRParams.training_object_y_size]
            ]
        )

        key = Interaction.quiz_answer()
        reaction_time = time() - start

        return key, reaction_time


    def present_quiz_phase2_question(self, object, options):

        start, reaction_time = time(), 0
        self.draw_multiple_images(
            [
                '{}{}.jpg'.format(TaskParams.image_dir, object),
                '{}{}.jpg'.format(TaskParams.image_dir, options[0]),
                '{}{}.jpg'.format(TaskParams.image_dir, options[1])
            ],
            [
                [SCRParams.quiz2_object_x_index, SCRParams.quiz2_object_y_index],
                [-SCRParams.quiz2_option_x_index, SCRParams.quiz2_option_y_index],
                [SCRParams.quiz2_option_x_index, SCRParams.quiz2_option_y_index]
            ],
            [
                [SCRParams.training_object_x_size, SCRParams.training_object_y_size],
                [SCRParams.option_x_size, SCRParams.option_y_size],
                [SCRParams.option_x_size, SCRParams.option_y_size]
            ]
        )

        key = Interaction.quiz_answer()
        reaction_time = time() - start

        return key, reaction_time
