from analysis.num_of_trials.analyse_single_subject import analyse_single_subject
from analysis.num_of_trials.filter_data import filtered_data


WINDOW_SIZE = 70
DIFF = 5


def main():

    subjects_data = filtered_data('data/')
    for id, subject_data in subjects_data.items():
            analyse_single_subject(subject_data, id, WINDOW_SIZE, DIFF)
