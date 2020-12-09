import matplotlib.pyplot as plt

from analysis.simulation_results.MB_behaviour import extract_MB_behavior_data


def plot_pure_MF_agent(data_path, subjectID):

    common1_unique0, common0_unique1, common0_unique0, common1_unique1 = \
        extract_MF_behavior_data(data_path, subjectID)

    fig = plt.figure('MF agent repeat probabilities')
    xs = [0, 1]
    ys = [common1_unique0, common1_unique1]
    plt.plot(xs, ys, label='common = 1')
    ys = [common0_unique0, common0_unique1]
    plt.plot(xs, ys, label='common = 0')

    plt.xticks(range(2), ['U=0', 'U=1'])
    plt.ylim([0, 1])
    plt.legend()

    plt.show()


def plot_pure_MB_agent(data_path, subjectID):

    common1, common0 = extract_MB_behavior_data(data_path, subjectID)

    fig = plt.figure('MB agent repeat probabilities')
    xs = [0, 1]
    ys = [common1, common0]
    plt.plot(xs, ys)

    plt.xticks(range(2), ['C=0', 'C=1'])
    plt.ylim([0, 1])

    plt.show()
