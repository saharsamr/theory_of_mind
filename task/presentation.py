from task.params.task_params import TaskParams
from tools.directory_files import get_file_names
from task.interactions import Interaction

from psychopy import visual, core, gui, event

from time import sleep, time


class PresentationClass:

    def __init__(self, screen_size):
        self.screen = visual.Window(screen_size, monitor="testMonitor", units="pix", fullscr=True)


    @staticmethod
    def present_info_box():

        dlg = gui.Dlg(title="Subject's Info")
        dlg.addField('Name:')
        dlg.addField('Age:')
        dlg.addField('Gender:', choices=['Male', 'Female', 'Other'])
        ok_data = dlg.show()

        if dlg.OK:
            return {'name': ok_data[0], 'age': ok_data[1], 'gender': ok_data[2]}
        return None


    def draw_image(self, image_path, pos=[0, 0], size=None, flip=True):

        image = visual.ImageStim(self.screen, image_path, pos=pos, size=size)
        image.draw()
        if flip:
            self.screen.flip()


    def draw_multiple_images(self, images_path, poses, sizes, flip=True):

        for path, pos, size in zip(images_path, poses, sizes):
            image = visual.ImageStim(self.screen, path, pos=pos, size=size)
            image.draw()
        if flip:
            self.screen.flip()


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


    def present_trial(self, options, objects, rewards, time_limit=float('inf')):

        start, reaction_time = time(), 0
        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, options[0]), '{}{}.jpg'.format(TaskParams.image_dir, options[1])],
            [[-200, 0], [200, 0]], [[300, 500], [300, 500]]
        )

        key = Interaction.option_select(time_limit)
        if not key:
            self.draw_image(TaskParams.image_dir+'faster.png', size=TaskParams.screen_size)
            sleep(TaskParams.feedback_duration)
            return key, float('inf')
        reaction_time = time() - start

        index = 0 if key == 'left' else 1
        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, options[0]), '{}{}.jpg'.format(TaskParams.image_dir, options[1])],
            [[-200, 0], [200, 0]], [[300, 500], [300, 500]], flip=False
        )
        self.draw_selected_rectangle(key)
        self.screen.flip()
        sleep(TaskParams.lag_to_response)

        self.present_objects_rewards(options[index], objects[index], rewards[index])

        return key, reaction_time


    def draw_selected_rectangle(self, key, color=[-1, 1, -1]):

        x1, y1, x2, y2 = (-360, 260, -40, -260) if key == 'left' else (40, 260, 360, -260)
        self.draw_rectangle(x1, y1, x2, y2, color)


    def present_agent_trial(self, options, selected, selected_objects, selected_rewards, time_limit=float('inf')):

        start, reaction_time = time(), 0
        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, options[0]), '{}{}.jpg'.format(TaskParams.image_dir, options[1])],
            [[-200, 0], [200, 0]], [[300, 500], [300, 500]]
        )
        key = Interaction.option_select(time_limit)

        reaction_time = time() - start

        self.present_objects_rewards(selected, selected_objects, selected_rewards)

        predicted_option = options[0] if key == 'left' else options[1]
        self.screen.flip()
        sleep(TaskParams.lag_to_response)
        self.present_prediction_reward(predicted_option, selected)

        return key, reaction_time


    def present_prediction_reward(self, predicted_option, selected_option):

        if predicted_option == selected_option:
            self.draw_image(TaskParams.image_dir+'fail.png', size=[500, 500])
        else:
            self.draw_multiple_images(
                [TaskParams.image_dir+'check.png', TaskParams.image_dir+'money.png'],
                [[0, 0], [-150, -150]], [[500, 500], [300, 300]]
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
                [[0, 100], [0, -350], [-275, -525]], [[200, 300], [700, 500], [150, 150]]
            )
            sleep(TaskParams.feedback_duration)

            if i == 0:
                self.draw_image('{}gray.png'.format(TaskParams.image_dir), flip=False)
                self.draw_image('{}{}.jpg'.format(TaskParams.image_dir, option), size=[200, 300], pos=[0, 100])
            else:
                self.draw_image('{}gray.png'.format(TaskParams.image_dir))

            sleep(TaskParams.clear_after_feedback)


    def present_instructions(self, related_phase):

        instruction_folder = TaskParams.instructions_path + related_phase + '/'
        images_name = sorted(get_file_names(instruction_folder, extention='png'))

        instruction_index, num_of_images = 0, len(images_name)
        while True:

            image = images_name[instruction_index]
            self.draw_image(instruction_folder+image, size=TaskParams.screen_size)

            key_list = Interaction.instrutions_allowed_keys(instruction_index, num_of_images)
            keys = event.waitKeys(keyList=key_list)

            instruction_index += 1 if keys[0] == 'left' else -1

            if keys[0] == 'space':
                break


    def present_training_step(self, option, objects):

        start, reaction_time = time(), 0
        self.draw_image(TaskParams.image_dir+str(option)+'.jpg', pos=[0, 550], size=[300, 500])
        if Interaction.ready_to_present_option_objects():
            reaction_time = time() - start
            sleep(TaskParams.lag_to_response)

        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, objects[0]), '{}{}.jpg'.format(TaskParams.image_dir, option)],
            [[0, 0], [0, 550]], [[700, 500], [300, 500]]
        )
        sleep(TaskParams.object_presentation_time_in_training)


        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, objects[1]), '{}{}.jpg'.format(TaskParams.image_dir, option)],
            [[0, 0], [0, 550]], [[700, 500], [300, 500]]
        )
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
            [[0,0], [-550, 0], [550, 0]], [[300, 500], [700, 500], [700, 500]]
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
            [[0,0], [-550, 0], [550, 0]], [[700, 500], [300, 500], [300, 500]]
        )

        key = Interaction.quiz_answer()
        reaction_time = time() - start

        return key, reaction_time
