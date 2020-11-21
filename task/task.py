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


    @staticmethod
    def start_task(presenter):

        selecteds, reaction_times = [], []
        for block in range(TaskParams.num_of_blocks):
            block_selected, block_reaction_time = [], []
            for t_index in range(TaskParams.num_of_block_trials):

                key, reaction_time = presenter.present_trial(
                    TrialsInfo.trials_pairs[block][t_index],
                    TrialsInfo.trials_availables_objects[block][t_index],
                    TrialsInfo.available_objects_actual_rewards[block][t_index]
                )
                block_selected.append(key)
                block_reaction_time.append(reaction_time)

            selecteds.append(block_selected)
            reaction_times.append(block_reaction_time)

        TaskLogics.save_tirals_properties(selecteds, reaction_times)
