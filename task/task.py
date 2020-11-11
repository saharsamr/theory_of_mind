from task.task_logics import TaskLogics
from task.params.task_params import TaskParams


class Task:

    @staticmethod
    def initialize():

        TaskLogics.pair_options()
        TaskLogics.assign_objects_to_options()
        TaskLogics.assign_trials_pairs()
        TaskLogics.set_available_objects_in_trials()
