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

            block_selected, block_reaction_time = Task.run_trials_block(
                presenter, TaskParams.num_of_block_trials,
                TrialsInfo.trials_pairs[block],
                TrialsInfo.trials_availables_objects[block],
                TrialsInfo.available_objects_actual_rewards[block],
                TaskParams.time_limit_for_selection
            )

            selecteds.append(block_selected)
            reaction_times.append(block_reaction_time)

        TaskLogics.save_tirals_properties(selecteds, reaction_times)


    @staticmethod
    def run_trials_block(
        presenter, num_block_trials, block_trial_pairs,
        block_available_objects, block_object_rewards, time_limit=float('inf')
    ):

        block_selected, block_reaction_time = [], []
        for t_index in range(num_block_trials):

            key, reaction_time = presenter.present_trial(
                block_trial_pairs[t_index],
                block_available_objects[t_index],
                block_object_rewards[t_index],
                time_limit
            )
            block_selected.append(key)
            block_reaction_time.append(reaction_time)

        return block_selected, block_reaction_time
