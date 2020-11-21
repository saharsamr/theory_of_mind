from task.task_logics import TaskLogics
from task.trials_info import TrialsInfo
from task.params.task_params import TaskParams


class Task:

    @staticmethod
    def initialize():

        TaskLogics.pair_options()
        TaskLogics.assign_objects_to_options()
        TaskLogics.assign_trials_pairs()
        TaskLogics.set_available_objects_in_trials()
        TaskLogics.set_objects_reward_probs_by_random_walk()
        TaskLogics.store_trials_available_objects_reward_prob()
        TaskLogics.set_objects_actual_rewards()
