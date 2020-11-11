from task.params.task_params import TaskParams


class TrialsInfo:

    trials_pairs = []
    trials_availables_objects = []


    @classmethod
    def set_trials_pairs(cls, trials_pairs):

        cls.trials_pairs = trials_pairs


    @classmethod
    def set_trials_available_objects(cls, objects):

        cls.trials_availables_objects = objects
