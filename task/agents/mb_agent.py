from task.params.task_params import TaskParams
from task.agents.agent import Agent


@Agent.register
class MBAgent(Agent):

    object_qvalues = {}


    @classmethod
    def initialize_qvalues(cls):

        for object in TaskParams.objects:
            cls.object_qvalues[object] = 0.5

        for option in TaskParams.first_options:
            cls.option_qvalues[option] = 1.0


    @classmethod
    def update_qvalues(cls, option, objects, rewards):

        cls.update_object_qvalues(objects[0], rewards[0])
        cls.update_object_qvalues(objects[1], rewards[1])
        cls.update_option_qvalues()


    @classmethod
    def update_object_qvalues(cls, object, reward):

        cls.object_qvalues[object] = \
        cls.object_qvalues[object] + cls.lr_param * (reward - cls.object_qvalues[object])


    @classmethod
    def update_option_qvalues(cls):

        for option in cls.option_qvalues.keys():

            objects = TaskParams.objects_of_options[option]
            cls.option_qvalues[option] = \
                cls.object_qvalues[objects[0]] + cls.object_qvalues[objects[1]]
