from task.params.task_params import TaskParams
from tools.directory_files import get_file_names
from task.interactions import Interaction

from psychopy import visual, core, gui, event


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


    def draw_image(self, image_path):

        image = visual.ImageStim(self.screen, image_path)
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
