from analysis.num_of_trials.analyse_single_subject import analyse_single_subject
from analysis.num_of_trials.filter_data import filtered_data
from analysis.num_of_trials.plot import plot_window_repeat_probs, plot_whole_repeat_probs, \
                                        plot_subject_windows_all_coefs


WINDOW_SIZE = 100
DIFF = 5


def main():

    subjects_data = filtered_data('data/')
    for id, subject_data in subjects_data.items():
            (probs, coefficients) = analyse_single_subject(subject_data, id, WINDOW_SIZE, DIFF)
            plot_subject_windows_all_coefs(coefficients, WINDOW_SIZE, DIFF)
            plot_whole_repeat_probs(probs, id)