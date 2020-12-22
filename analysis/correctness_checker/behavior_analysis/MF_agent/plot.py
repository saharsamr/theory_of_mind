import matplotlib.pyplot as plt

from analysis.correctness_checker.behavior_analysis.MF_agent.MF_behaviour import \
    extract_MF_behavior_data, extract_data_MF_glmfit
from analysis.correctness_checker.behavior_analysis.MF_agent.MF_behaviour import \
    find_repeat_probs as find_repeat_probs_MF, extract_MF_probabilities
from tools.directory_files import get_directory_names


def pulled_MF_result(data_path, alpha, beta):

    data_path += 'alpha{}beta{}/'.format(alpha, beta)
    subject_models, subject_results, pulled_model, pulled_results = \
        extract_data_MF_glmfit(data_path)
    print(pulled_results.summary())

    plot_pulled_prob_MF_agent(data_path)


def plot_pulled_prob_MF_agent(data_path):

    subjectd_IDs = get_directory_names(data_path)
    for id in subjectd_IDs:

        repeat, common_rewarded, unique_rewarded = extract_MF_behavior_data(data_path, id)
        common1_unique0, common0_unique1, common0_unique0, common1_unique1 = \
            find_repeat_probs_MF(repeat, common_rewarded, unique_rewarded)

        fig = plt.figure('MF agent repeat probabilities')
        xs = [0, 1]
        ys = [common1_unique0, common1_unique1]
        plt.scatter(xs, ys, c='b', linewidths=0.5, marker='.', s=3)
        ys = [common0_unique0, common0_unique1]
        plt.scatter(xs, ys, c='r', linewidths=0.5, marker='.', s=3)

        plt.xticks(range(2), ['U=0', 'U=1'])
        plt.ylim([0, 1])

    mean_c1u1, std_c1u1, mean_c1u0, std_c1u0, mean_c0u1, std_c0u1, mean_c0u0, std_c0u0 = \
        extract_MF_probabilities(data_path)

    plt.errorbar(xs, [mean_c0u0, mean_c0u1], yerr=[std_c0u0, std_c0u1], label='common 0')
    plt.errorbar(xs, [mean_c1u0, mean_c1u1], yerr=[std_c1u0, std_c1u1], label='common 1')
    plt.legend()
    plt.ylabel('Prob(repeat)')

    plt.show()
