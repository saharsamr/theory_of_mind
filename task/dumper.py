from task.trials_info import TrialsInfo as Trials
from task.params.task_params import TaskParams
from task.params.subject_params import SubjectParams
from task.trainer import Trainer

import json


class Dumper:

    @staticmethod
    def save_params(path, file_name):

        with open('{}{}.json'.format(path, file_name), mode='w') as param_file:

            params = {
                'date': SubjectParams.subject_date.strftime("%m/%d/%Y, %H:%M:%S"),
                'subjectID': SubjectParams.subject_id,
                'age': SubjectParams.subject_age,
                'gender': SubjectParams.subject_gender,
                'option_pairs': TaskParams.options_pairs,
                'objects_of_options': TaskParams.objects_of_options
            }

            json.dump(params, param_file)


    @staticmethod
    def save_phase_data(path, file_name, is_prediction=False, agent=None):

        with open('{}{}.json'.format(path, file_name), mode='w') as data_file:

            trials = []
            for block in range(TaskParams.num_of_blocks):
                for trial in range(TaskParams.num_of_block_trials):

                    row = {
                        'options': Trials.trials_pairs[block][trial],
                        'possible_objects': Trials.trials_availables_objects[block][trial],
                        'all_reward_probs': Trials.objects_reward_probs_during_trials[block][trial],
                        'possible_reward_probs': Trials.trials_availables_objects_reward_probs[block][trial],
                        'generated_randoms': Trials.generated_randoms_for_rewards[block][trial],
                        'possible_actual_rewards': Trials.available_objects_actual_rewards[block][trial],
                        'selected_option': Trials.subject_selected_options[block][trial],
                        'visited_objects': None if not Trials.visited_objects[block][trial] else\
                            [int(o) for o in Trials.visited_objects[block][trial]],
                        'gained_rewards': None if not Trials.objects_gained_rewards[block][trial] else\
                            [int(r) for r in Trials.objects_gained_rewards[block][trial]],
                        'reaction_times': Trials.selection_reaction_times[block][trial]
                    }
                    if is_prediction:
                        row['predictions'] = Trials.subject_predictions[block][trial]
                        row['agent'] = agent

                    trials.append(row)

            json.dump(trials, data_file)


    @staticmethod
    def save_training_data(path, file_name):

        with open('{}{}.json'.format(path, file_name), mode='w') as data_file:

            exercices = []
            for round in range(len(Trainer.training_options_order)):
                for index in range(len(Trainer.training_options_order[round])):

                    row = {
                        'round': round,
                        'options': Trainer.training_options_order[round][index],
                        'objects_orders': Trainer.objects_presentation_order[round][index],
                        'reaction_times': Trainer.presentation_response_times[round][index]
                    }

                    exercices.append(row)

            json.dump(exercices, data_file)


    @staticmethod
    def save_quiz_phase1_data(path, file_name):

        with open('{}{}.json'.format(path, file_name), mode='w') as data_file:

            exercices = []
            for round in range(len(Trainer.options_of_quiz_phase1)):
                for index in range(len(Trainer.options_of_quiz_phase1[round])):

                    row = {
                        'round': round,
                        'options': Trainer.options_of_quiz_phase1[round][index],
                        'objects_orders': Trainer.objects_of_quiz_phase1[round][index],
                        'reponses': Trainer.quiz_phase1_responses[round][index],
                        'reaction_times': Trainer.quiz_phase1_response_times[round][index]
                    }

                    exercices.append(row)

            json.dump(exercices, data_file)


    @staticmethod
    def save_quiz_phase2_data(path, file_name):

        with open('{}{}.json'.format(path, file_name), mode='w') as data_file:

            exercices = []
            for round in range(len(Trainer.options_of_quiz_phase2)):
                for index in range(len(Trainer.options_of_quiz_phase2[round])):

                    row = {
                        'round': round,
                        'options': Trainer.options_of_quiz_phase2[round][index],
                        'objects_orders': Trainer.objects_of_quiz_phase2[round][index],
                        'reponses': Trainer.quiz_phase2_responses[round][index],
                        'reaction_times': Trainer.quiz_phase2_response_times[round][index]
                    }

                    exercices.append(row)

            json.dump(exercices, data_file)


    @staticmethod
    def save_warmup_data(path, file_name):

        with open('{}{}.json'.format(path, file_name), mode='w') as data_file:

            trials = []
            for index in range(len(Trials.warmup_trials_pairs)):

                row = {
                    'options': Trials.warmup_trials_pairs[index],
                    'possible_objects': Trials.warmup_available_objects[index],
                    'possible_reward_probs': Trials.warmup_reward_probs[index],
                    'generated_randoms': Trials.warmup_generated_randoms[index],
                    'possible_actual_rewards': Trials.warmup_objects_actual_rewards[index],
                    'selected_option': Trials.warmup_subject_selections[index],
                    'visited_objects': [int(o) for o in Trials.warmup_visited_objects[index]],
                    'gained_rewards': [int(r) for r in Trials.warmup_gained_rewards[index]],
                    'reaction_times': Trials.warmup_selection_reaction_times[index]
                }

                trials.append(row)

            json.dump(trials, data_file)
