from analysis.num_of_trials.analyse_single_subject import analyse_single_subject
from analysis.num_of_trials.filter_data import filtered_data
from analysis.num_of_trials.plot import plot_sub_repeat_probs, plot_whole_repeat_probs


WINDOW_SIZE = 100
DIFF = 10


def main():

    subjects_data = filtered_data('data/')
    for id, subject_data in subjects_data.items():
            probs = analyse_single_subject(subject_data, id, WINDOW_SIZE, DIFF)
            plot_whole_repeat_probs(probs, id)
            plot_sub_repeat_probs(probs, WINDOW_SIZE, DIFF, id)
