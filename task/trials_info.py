from task.params.task_params import TaskParams


class TrialsInfo:

    trials_pairs = []
    trials_availables_objects = []
    objects_reward_probs_during_trials = []
    trials_availables_objects_reward_probs = []
    generated_randoms_for_rewards = []
    available_objects_actual_rewards = []

    subject_selected_options = []
    visited_objects = []
    objects_gained_rewards = []
    selection_reaction_times = []


    @classmethod
    def set_trials_pairs(cls, trials_pairs):

        cls.trials_pairs = trials_pairs


    @classmethod
    def set_trials_available_objects(cls, objects):

        cls.trials_availables_objects = objects


    @classmethod
    def set_objects_reward_probs(cls, reward_probs):

        cls.objects_reward_probs_during_trials = reward_probs


    @classmethod
    def set_available_objects_reward_probs(cls, reward_probs):

        cls.trials_availables_objects_reward_probs = reward_probs


    @classmethod
    def set_objects_actual_rewards(cls, rewards):

        cls.available_objects_actual_rewards = rewards


    @classmethod
    def set_generated_randoms_for_rewards(cls, randoms):

        cls.generated_randoms_for_rewards = randoms


    @classmethod
    def set_subjects_selection(cls, selections):

        cls.subject_selected_options = selections


    @classmethod
    def set_visited_objects(cls, objects):

        cls.visited_objects = objects


    @classmethod
    def set_gained_rewards(cls, rewards):

        cls.objects_gained_rewards = rewards


    @classmethod
    def set_selection_reaction_times(cls, reaction_times):

        cls.selection_reaction_times = reaction_times
