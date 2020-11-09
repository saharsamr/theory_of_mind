from task.params.task_params import TaskParams
from tools.directory_files import get_file_names
from task.interactions import Interaction

from psychopy import visual, core, gui, event

from time import sleep


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


    def draw_image(self, image_path, pos=[0, 0], size=None):

        image = visual.ImageStim(self.screen, image_path, pos=pos, size=size)
        image.draw()
        self.screen.flip()


    def draw_multiple_images(self, images_path, poses, sizes):

        for path, pos, size in zip(images_path, poses, sizes):
            image = visual.ImageStim(self.screen, path, pos=pos, size=size)
            image.draw()

        self.screen.flip()


    def present_instructions(self, related_phase):

        instruction_folder = TaskParams.instructions_path + related_phase + '/'
        images_name = sorted(get_file_names(instruction_folder))

        instruction_index, num_of_images = 0, len(images_name)
        while True:

            image = images_name[instruction_index]
            self.draw_image(instruction_folder+image)

            key_list = Interaction.instrutions_allowed_keys(instruction_index, num_of_images)
            keys = event.waitKeys(keyList=key_list)

            instruction_index += 1 if keys[0] == 'left' else -1

            if keys[0] == 'space':
                break


    def present_training_step(self, option, objects):

        self.draw_image(TaskParams.image_dir+str(option)+'.jpg', pos=[0, 550], size=[300, 500])
        if Interaction.ready_to_present_option_objects():
            sleep(TaskParams.lag_to_response)

        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, objects[0]), '{}{}.jpg'.format(TaskParams.image_dir, option)],
            [[0, 0], [0, 550]], [[600, 400], [300, 500]]
        )
        sleep(TaskParams.object_presentation_time_in_training)


        self.draw_multiple_images(
            ['{}{}.jpg'.format(TaskParams.image_dir, objects[1]), '{}{}.jpg'.format(TaskParams.image_dir, option)],
            [[0, 0], [0, 550]], [[600, 400], [300, 500]]
        )
        sleep(TaskParams.object_presentation_time_in_training)

        self.draw_image(TaskParams.image_dir+'gray.png')
        sleep(0.25)
