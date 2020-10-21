from analysis.num_of_trials.analyse_single_subject import analyse_single_subject
from analysis.num_of_trials.filter_data import filtered_data
from analysis.num_of_trials.plot import plot_window_repeat_probs, plot_whole_repeat_probs, \
                                        plot_subject_windows_all_coefs, plot_differece_means
from analysis.num_of_trials.analyse_all_data import calc_difference_means_with_error_bar, \
                                                    t_test_on_differences
from analysis.num_of_trials.print_results import print_windows_ttest_results


WINDOW_SIZE = 100
DIFF = 5


def main():

    subjects_data = filtered_data('data/')
    subjects_coefficients = {}
    for id, subject_data in subjects_data.items():
        print('*****************************************Subject#{}*****************************************'.format(int(id)))
        (probs, coefficients) = analyse_single_subject(subject_data, id, WINDOW_SIZE, DIFF)
        subjects_coefficients[id] = coefficients
        plot_subject_windows_all_coefs(coefficients, WINDOW_SIZE, DIFF, id)
        plot_whole_repeat_probs(probs, id)

    differences_data, vectorize_differences = calc_difference_means_with_error_bar(subjects_coefficients, WINDOW_SIZE, DIFF)
    plot_differece_means(differences_data, WINDOW_SIZE, DIFF)
    ttest_result = t_test_on_differences(vectorize_differences)
    print_windows_ttest_results(ttest_result, WINDOW_SIZE, DIFF)
