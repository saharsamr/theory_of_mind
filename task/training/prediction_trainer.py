from task.params.task_params import TaskParams
from task.task_logics import TaskLogics

import random


class PredictionTrainer:

    num_training_repeat = 1

    trial_pairs = []
    available_objects = []
    rewards = []
    agent_selections = []
    user_predictions = []
    objects_actual_rewards = []

    agent_selection_responses = []
    user_prediction_responses = []

    @classmethod
    def start_training(cls, presenter):

        passed, round_ = False, 0
        while not passed:
            cls.set_round_info()
            agent_selections, user_selections = \
                cls.run_training_round(
                    presenter, 4*cls.num_training_repeat,
                    cls.trial_pairs[round_], cls.available_objects[round_],
                    cls.agent_selections[round_], cls.rewards[round_]
            )
            cls.user_prediction_responses.append(user_selections)
            cls.agent_selection_responses.append(agent_selections)

            passed = cls.is_passed(agent_selections, user_selections, round_)
            round_ += 1

    @classmethod
    def is_passed(cls, agent_selection_responses, user_selection_responses, round_):

        if agent_selection_responses == cls.agent_selections[round_] \
                and user_selection_responses == cls.user_predictions[round_]:

            same_selection, different_selections = False, False
            for agent, user in zip(cls.agent_selections[round_], cls.user_predictions[round_]):
                if same_selection and different_selections:
                    break
                if agent == user:
                    same_selection = True
                else:
                    different_selections = True

            return same_selection == different_selections

        return False

    @classmethod
    def run_training_round(
            cls, presenter, n_trials, trial_pairs, available_objects,
            real_selections, rewards, time_limit=float('inf')
    ):

        agent_selection_response, user_selection_response, user_predictions = [], [], []
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
            agent_selection_response.append(agent_selected)
            user_selection_response.append(user_selected)

        cls.user_predictions.append(user_predictions)
        return agent_selection_response, user_selection_response

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

        trial_pairs = []
        for _ in range(cls.num_training_repeat):
            trial_pairs.extend(TaskParams.options_pairs)
        random.shuffle(trial_pairs)
        available_objects = TaskLogics.find_available_objects(trial_pairs)
        reward_probs = TaskLogics.select_reward_prob_for_training(4*cls.num_training_repeat)
        generated_randoms, rewards = TaskLogics.set_reward(reward_probs)
        agent_selections = [options[random.choice([0, 1])] for options in trial_pairs]

        return trial_pairs, available_objects, rewards, agent_selections





