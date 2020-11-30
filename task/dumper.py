from task.trials_info import TrialsInfo as Trials
from task.params.task_params import TaskParams
from task.params.subject_params import SubjectParams
from task.trainer import Trainer

import csv


class Dumper:

    @staticmethod
    def save_params(paht, file_name):

        with open('{}{}.params'.format(path, file_name), mode='w') as param_file:

            param_file.write('date:{}\n'.format(SubjectParams.subject_date))
            param_file.write('subjectID:{}\n'.format(SubjectParams.subject_id))
            param_file.write('age:{}\n'.format(SubjectParams.subject_age))
            param_file.write('gender:{}\n'.format(SubjectParams.subject_gender))

            param_file.write('options_pairs:{}\n'.format(TaskParams.options_pairs))
            param_file.write('objects_of_options:{}\n'.format(TaskParams.objects_of_options))


    @staticmethod
    def save_phase_data(path, file_name, is_prediction=False):

        with open('{}{}.csv'.format(path, file_name), mode='w') as data_file:

            field_names = [
                'options', 'possible_objects', 'all_reward_probs',
                'possible_reward_probs', 'generated_randoms',
                'possible_actual_rewards', 'selected_option',
                'visited_objects', 'gained_rewards', 'reaction_times'
            ]
            if is_prediction:
                field_names.append('predictions')

            writer = csv.DictWriter(data_file, field_names=field_names)
            writer.writeheader()

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
                        'visited_objects': Trials.visited_objects[block][trial],
                        'gained_rewards': Trials.objects_gained_rewards[block][trial],
                        'reaction_times': Trials.selection_reaction_times[block][trial]
                    }
                    if is_prediction:
                        row['predictions'] = Trials.subject_predictions[block][trial]

                    writer.writerow(row)


    @staticmethod
    def save_training_data(path, file_name):

        with open('{}{}.csv'.format(path, file_name), mode='w') as data_file:

            field_names = [
                'round', 'options', 'objects_orders', 'reaction_times'
            ]

            writer = csv.DictWriter(data_file, field_names=field_names)
            writer.writeheader()

            for round in range(len(Trainer.training_options_order)):
                for index in range(len(Trainer.training_options_order[round])):

                    row = {
                        'round': round,
                        'options': Trainer.training_options_order[round][index],
                        'objects_orders': Trainer.objects_presentation_order[round][index],
                        'reaction_times': Trainer.presentation_response_times[round][index]
                    }

                    writer.writerow(row)


    @staticmethod
    def save_quiz_phase1_data(path, file_name):

        with open('{}{}.csv'.format(path, file_name), mode='w') as data_file:

            field_names = [
                'round', 'options', 'objects_orders', 'reponses', 'reaction_times'
            ]

            writer = csv.DictWriter(data_file, field_names=field_names)
            writer.writeheader()

            for round in range(len(Trainer.options_of_quiz_phase1)):
                for index in range(len(Trainer.options_of_quiz_phase1[round])):

                    row = {
                        'round': round,
                        'options': Trainer.options_of_quiz_phase1[round][index],
                        'objects_orders': Trainer.objects_of_quiz_phase1[round][index],
                        'reponses': Trainer.quiz_phase1_responses[round][index],
                        'reaction_times': Trainer.quiz_phase1_response_times[round][index]
                    }

                    writer.writerow(row)


    @staticmethod
    def save_quiz_phase2_data(path, file_name):

        with open('{}{}.csv'.format(path, file_name), mode='w') as data_file:

            field_names = [
                'round', 'options', 'objects_orders', 'reponses', 'reaction_times'
            ]

            writer = csv.DictWriter(data_file, field_names=field_names)
            writer.writeheader()

            for round in range(len(Trainer.options_of_quiz_phase2)):
                for index in range(len(Trainer.options_of_quiz_phase2[round])):

                    row = {
                        'round': round,
                        'options': Trainer.options_of_quiz_phase2[round][index],
                        'objects_orders': Trainer.objects_of_quiz_phase2[round][index],
                        'reponses': Trainer.quiz_phase2_responses[round][index],
                        'reaction_times': Trainer.quiz_phase2_response_times[round][index]
                    }

                    writer.writerow(row)


    @staticmethod
    def save_warmup_data(path, file_name):

        with open('{}{}.csv'.format(path, file_name), mode='w') as data_file:

            field_names = [
                'options', 'possible_objects', 'possible_reward_probs',
                'generated_randoms', 'possible_actual_rewards',
                'selected_option', 'visited_objects', 'gained_rewards',
                'reaction_times'
            ]

            writer = csv.DictWriter(data_file, field_names=field_names)
            writer.writeheader()

            for index in range(len(Trainer.options_of_quiz_phase2[round])):

                row = {
                    'options': Trials.warmup_trials_pairs[index],
                    'possible_objects': Trials.warmup_available_objects[index],
                    'possible_reward_probs': Trials.warmup_reward_probs[index],
                    'generated_randoms': Trials.warmup_generated_randoms[index],
                    'possible_actual_rewards': Trials.warmup_objects_actual_rewards[index],
                    'selected_option': Trials.warmup_subject_selections[index],
                    'visited_objects': Trials.warmup_visited_objects[index],
                    'gained_rewards': Trials.warmup_gained_rewards[index],
                    'reaction_times': Trials.warmup_selection_reaction_times[index]
                }

                writer.writerow(row)
