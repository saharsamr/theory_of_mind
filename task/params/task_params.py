from pathlib import Path

class TaskParams:

    screen_size = [2736, 1824]

    data_dir = 'task/data/'
    image_dir = 'task/images/'
    instructions_path = 'task/instructions/'
    random_walks_path = 'task/random_walks/'

    first_options = (0, 1, 2, 3)
    second_options = (0, 1, 2, 3)
    objects = (10, 11, 12, 13)

    options_pairs = None
    objects_of_options = None

    lag_to_response = 0.5
    object_presentation_time_in_training = 1.0
    time_limit_for_quiz = 3.0
    time_limit_training_question = 3.0
    feedback_duration = 1.0
    clear_after_feedback = 0.1
    time_limit_for_selection = 2.0
    time_limit_for_prediction = 3.0
    time_for_rest = 60.0
    n_random_walks = 6

    min_time_for_agent_selection = 0.5

    n_warm_up_trials = 8
    n_prediction_training_trials = 8
    num_of_blocks = 3
    num_of_block_trials = 60
    n_trials = 3 * 60

    n_agent_blocks = 3
    n_agent_block_trials = 60
    n_agent_trials = 3 * 60

    init_block_probs = [0.2, 0.4, 0.6, 0.8]
    reward_prob_std = 0.03
    max_reward_prob = 0.8
    min_reward_prob = 0.2


    @classmethod
    def set_options_pairs(cls, pairs):
        cls.options_pairs = pairs


    @classmethod
    def set_objects_of_options(cls, objects_of_options):
        cls.objects_of_options = objects_of_options


    @classmethod
    def set_subject_data_dir(cls, id):

        cls.data_dir = cls.data_dir+str(id)+'/'
        Path(cls.data_dir).mkdir(parents=True, exist_ok=True)
