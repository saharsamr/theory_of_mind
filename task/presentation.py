from psychopy import visual, core, gui


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
