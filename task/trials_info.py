from task.params.task_params import TaskParams


class TrialsInfo:

    trials_pairs = []
    trials_availables_objects = []
    objects_reward_probs_during_trials = []
    trials_availables_objects_reward_probs = []
    generated_randoms_for_rewards = []
    available_objects_actual_rewards = []

    warmup_trials_pairs = []
    warmup_available_objects = []
    warmup_reward_probs = []
    warmup_generated_randoms = []
    warmup_objects_actual_rewards = []

    subject_selected_options = []
    visited_objects = []
    objects_gained_rewards = []
    selection_reaction_times = []
    subject_predictions = []

    warmup_subject_selections = []
    warmup_visited_objects = []
    warmup_gained_rewards = []
    warmup_selection_reaction_times = []


    @classmethod
    def reinitialize_trials_info(cls):

        cls.trials_pairs = []
        cls.trials_availables_objects = []
        cls.objects_reward_probs_during_trials = []
        cls.trials_availables_objects_reward_probs = []
        cls.generated_randoms_for_rewards = []
        cls.available_objects_actual_rewards = []

        cls.subject_selected_options = []
        cls.visited_objects = []
        cls.objects_gained_rewards = []
        cls.selection_reaction_times = []
        cls.subject_predictions = []


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

    @classmethod
    def set_subject_predictions(cls, predictions):

        cls.subject_predictions = predictions


    @classmethod
    def sample_for_warmup(cls, sampling_indices):

        import numpy as np

        cls.warmup_trials_pairs = np.array(cls.trials_pairs[0])[sampling_indices]
        cls.warmup_available_objects = np.array(cls.trials_availables_objects[0])[sampling_indices]
        cls.warmup_reward_probs = np.array(cls.trials_availables_objects_reward_probs[0])[sampling_indices]


    @classmethod
    def set_rewards_for_warmup(cls, generated_randoms, actual_rewards):

        cls.warmup_generated_randoms = generated_randoms
        cls.warmup_objects_actual_rewards = actual_rewards


    @classmethod
    def set_warmup_selections(cls, selections):

        cls.warmup_subject_selections = selections


    @classmethod
    def set_warmup_visited_objects(cls, visited_objects):

        cls.warmup_visited_objects = visited_objects


    @classmethod
    def set_warmup_gained_rewards(cls, rewards):

        cls.warmup_gained_rewards = rewards


    @classmethod
    def set_warmup_reaction_times(cls, reaction_times):

        cls.warmup_selection_reaction_times = reaction_times
