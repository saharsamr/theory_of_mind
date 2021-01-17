from task.presentation import PresentationClass
from task.params.subject_params import SubjectParams
from task.params.task_params import TaskParams
from task.task import Task
from task.training.trainer import Trainer
from task.training.prediction_trainer import PredictionTrainer
from task.agents.mf_agent import MFAgent
from task.agents.mb_agent import MBAgent
from task.dumper import Dumper

import random


def main():

    presenter = PresentationClass(screen_size=TaskParams.screen_size)

    subject_info = presenter.present_info_box()
    SubjectParams.set_subject_info(subject_info)
    TaskParams.set_subject_data_dir(SubjectParams.subject_id)
    Dumper.save_params(TaskParams.data_dir, '{}-params'.format(SubjectParams.subject_id))

    Task.initialize()

    presenter.present_instructions('start-training')
    Trainer.start_training(presenter)
    Dumper.save_training_data(TaskParams.data_dir, '{}-training'.format(SubjectParams.subject_id))
    Dumper.save_quiz_phase1_data(TaskParams.data_dir, '{}-quiz-phase1'.format(SubjectParams.subject_id))
    Dumper.save_quiz_phase2_data(TaskParams.data_dir, '{}-quiz-phase2'.format(SubjectParams.subject_id))

    PredictionTrainer.start_training(presenter)

    presenter.present_instructions('phase1')
    Task.run_warm_up_block(presenter)
    Dumper.save_warmup_data(TaskParams.data_dir, '{}-warmup'.format(SubjectParams.subject_id))

    presenter.present_instructions('start-task')
    Task.start_task(presenter)
    Dumper.save_phase_data(TaskParams.data_dir, '{}-task-phase1'.format(SubjectParams.subject_id))

    presenter.present_instructions('phase2')
    agent, agent_name = (MFAgent, 'MF') if random.random() < 0.5 else (MBAgent, 'MB')
    agent.initialize_trials()
    agent.start_agent_task(presenter)
    Dumper.save_phase_data(TaskParams.data_dir, '{}-task-phase2'.format(SubjectParams.subject_id), is_prediction=True, agent=agent_name)

    presenter.present_instructions('phase3')
    Task.initialize(first_phase=False, phase=3)
    Task.start_task(presenter)
    Dumper.save_phase_data(TaskParams.data_dir, '{}-task-phase3'.format(SubjectParams.subject_id))
