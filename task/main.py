from task.presentation import PresentationClass
from task.params.subject_params import SubjectParams
from task.task import Task
from task.trainer import Trainer

from psychopy import gui, core


def main():

    presenter = PresentationClass(screen_size=[2736, 1824])

    subject_info = presenter.present_info_box()
    SubjectParams.set_subject_info(subject_info)

    Task.initialize()
    Trainer.start_training(presenter)

    presenter.present_instructions('task_description')
