from task.params.task_params import TaskParams

import random


class PredictionTrainer:

    num_training_repeat = 1

    trial_pairs = []
    available_objects = []
    rewards = []
    agent_selections = []
    objects_actual_rewards = []

    @classmethod
    def start_training(cls, presenter):

        passed, round_ = False, 0
        while not passed:
            cls.set_round_info()
            agent_selections, user_selections, user_predictions = \
                cls.run_training_round(
                    presenter, 4*cls.num_training_repeat,
                    cls.trial_pairs[round_], cls.available_objects[round_],
                    cls.agent_selections[round_], cls.rewards[round_]
            )

            if agent_selections == cls.agent_selections[round_] and user_predictions == user_selections:
                passed = True

    @classmethod
    def run_training_round(
            cls, presenter, n_trials, trial_pairs, available_objects,
            real_selections, rewards, time_limit=float('inf')
    ):

        agent_selections, user_selections, reaction_times, user_predictions = [], [], [], []
        for t in range(n_trials):

            real_selected_index = 0 if trial_pairs[t][0] == real_selections[t] else 1
            key, _ = presenter.present_agent_trial(
                trial_pairs[t], real_selections[t],
                available_objects[t][real_selected_index],
                rewards[t][real_selected_index]
            )
            prediction = trial_pairs[t][0] if key == 'left' else trial_pairs[t][1]
            user_predictions.append(prediction)
            agent_selected, user_selected = \
                presenter.present_prediction_training_step(
                    trial_pairs[t], real_selections[t], prediction, time_limit
            )
            agent_selections.append(agent_selected)
            user_selections.append(user_selected)

        return agent_selections, user_selections, user_predictions

    @classmethod
    def set_round_info(cls):

        trial_pairs, available_objects, rewards, agent_selections = \
            cls.manage_training_trials()
        cls.trial_pairs.append(trial_pairs)
        cls.available_objects.append(available_objects)
        cls.rewards.append(rewards)
        cls.agent_selections.append(agent_selections)

    @classmethod
    def manage_training_trials(cls):

        trial_pairs = [random.choice(TaskParams.options_pairs) for _ in range(4*cls.num_training_repeat)]
        available_objects = [
            [
                TaskParams.objects_of_options[options[0]],
                TaskParams.objects_of_options[options[1]]
            ] for options in trial_pairs
        ]
        rewards = [
            [
                (random.choice([0, 1]), random.choice([0, 1])),
                (random.choice([0, 1]), random.choice([0, 1]))
            ]
            for options in trial_pairs
        ]
        agent_selections = [options[random.choice([0, 1])] for options in trial_pairs]

        return trial_pairs, available_objects, rewards, agent_selections




