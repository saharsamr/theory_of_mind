from task.params.task_params import TaskParams


class Agent:

    mf_qvalues = {}
    mb_qvalues = {}


    @classmethod
    def initial_mf_qvalues(cls):

        for option in TaskParams.first_options:
            cls.mf_qvalues[option] = 1.0


    @classmethod
    def initial_mb_qvalues(cls):

        for object in TaskParams.objects:
            cls.mb_qvalues[object] = 0.5
