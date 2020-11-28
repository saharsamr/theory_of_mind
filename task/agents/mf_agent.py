from task.params.task_params import TaskParams
from task.agents.agent import Agent


@Agent.register
class MFAgent(Agent):

    @classmethod
    def initialize_qvalues(cls):

        for option in TaskParams.first_options:
            cls.option_qvalues[option] = 1.0


    @classmethod
    def update_qvalues(cls, option, objects, rewards):
        
        total_reward = sum(rewards)
        cls.update_option_qvalues(option, total_reward)


    @classmethod
    def update_option_qvalues(cls, option, reward):

        cls.option_qvalues[option] = \
            cls.option_qvalues[option] + cls.lr_param * (reward - cls.option_qvalues[option])
