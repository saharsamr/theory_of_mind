import matplotlib.pyplot as plt

from analysis.correctness_checker.behavior_analysis.MB_agent.MB_behaviour import \
    extract_MB_behavior_data, extract_data_MB_glmfit
from analysis.correctness_checker.behavior_analysis.MB_agent.MB_behaviour import \
    find_repeat_probs as find_repeat_probs_MB, extract_MB_probabilities
from tools.directory_files import get_directory_names


def pulled_MB_result(data_path, alpha, beta):

    data_path += 'alpha{}beta{}/'.format(alpha, beta)
    subject_models, subject_results, pulled_model, pulled_results = \
        extract_data_MB_glmfit(data_path)
    print(pulled_results.summary())

    plot_pulled_prob_MB_agent(data_path)


def plot_pulled_prob_MB_agent(data_path):

    subjectd_IDs = get_directory_names(data_path)
    for id in subjectd_IDs:

        repeat, common_rewarded, _ = extract_MB_behavior_data(data_path, id)
        common1, common0 = find_repeat_probs_MB(repeat, common_rewarded)

        fig = plt.figure('MB agent repeat probabilities')
        xs = [0, 1]
        ys = [common0, common1]
        plt.scatter(xs, ys, c='b', linewidths=0.5, marker='.', s=3)

    plt.xticks(range(2), ['C=0', 'C=1'])
    plt.ylim([0, 1])

    mean_c1, std_c1, mean_c0, std_c0 = extract_MB_probabilities(data_path)

    plt.errorbar(xs, [mean_c0, mean_c1], yerr=[std_c0, std_c1])
    plt.ylabel('Prob(repeat)')

    plt.show()
