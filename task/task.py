from task.task_logics import TaskLogics
from task.trials_info import TrialsInfo
from task.params.task_params import TaskParams


class Task:

    @staticmethod
    def initialize(first_phase=True, phase=1):

        TrialsInfo.reinitialize_trials_info()

        if first_phase:
            TaskLogics.pair_options()
            TaskLogics.assign_objects_to_options()

        TaskLogics.assign_trials_pairs()
        TaskLogics.set_available_objects_in_trials()
        TaskLogics.set_objects_reward_probs(phase)
        TaskLogics.store_trials_available_objects_reward_prob()
        TaskLogics.set_objects_actual_rewards()

        if first_phase:
            TaskLogics.manage_warmup_trials()
            TaskLogics.set_rewards_for_warmup()


    @staticmethod
    def run_warm_up_block(presenter):

        warmup_selected, warmup_reaction_times = Task.run_trials_block(
            presenter, TaskParams.n_warm_up_trials,
            TrialsInfo.warmup_trials_pairs,
            TrialsInfo.warmup_available_objects,
            TrialsInfo.warmup_objects_actual_rewards,
        )

        TaskLogics.save_warmup_results(warmup_selected, warmup_reaction_times)



    @staticmethod
    def start_task(presenter):

        selecteds, reaction_times = [], []
        for block in range(TaskParams.num_of_blocks):

            if len(selecteds) != 0:
                presenter.present_rest()
                presenter.present_instructions('next-block')

            block_selected, block_reaction_time = Task.run_trials_block(
                presenter, TaskParams.num_of_block_trials,
                TrialsInfo.trials_pairs[block],
                TrialsInfo.trials_availables_objects[block],
                TrialsInfo.available_objects_actual_rewards[block],
                TaskParams.time_limit_for_selection
            )

            selecteds.append(block_selected)
            reaction_times.append(block_reaction_time)

        TaskLogics.save_trials_results(selecteds, reaction_times)


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
