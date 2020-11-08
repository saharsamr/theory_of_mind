from task.presentation import PresentationClass
from task.params.subject_params import SubjectParams

from psychopy import gui, core


def main():

    presenter = PresentationClass(screen_size=[2736, 1824])

    subject_info = presenter.present_info_box()
    SubjectParams.set_subject_info(subject_info)

    presenter.present_instructions('task_description')
