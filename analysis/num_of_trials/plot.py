import matplotlib.pyplot as plt
import numpy as np


N_TRIALS = 300


def plot_MF_probs(axs, repeat_probs, start=0, window_size=N_TRIALS):

    xs = [0, 1]
    probs = repeat_probs['model_free'][(start, start+window_size)]
    ys = [probs['common1_unique0'], probs['common1_unique1']]
    axs.plot(xs, ys, label='common = 1')
    ys = [probs['common0_unique0'], probs['common0_unique1']]
    axs.plot(xs, ys, label='common = 0')

    axs.set_xticks(range(2))
    axs.set_xticklabels(['U=0', 'U=1'])
    axs.set_ylim([0, 1])
    axs.legend()


def plot_MB_probs(axs, repeat_probs, start=0, window_size=N_TRIALS):

    xs = [0, 1]
    probs = repeat_probs['model_based'][(start, start+window_size)]
    ys = [probs['common0'], probs['common1']]
    axs.plot(xs, ys)
    axs.set_xticks(range(2))
    axs.set_xticklabels(['C=0', 'C=1'])
    axs.set_ylim([0, 1])


def plot_whole_repeat_probs(repeat_probs, subject_ID):

    fig, axs = plt.subplots(1, 2)
    fig.suptitle('Subject#{}'.format(int(subject_ID)))

    axs[0].set_title('Model Free')
    plot_MF_probs(axs[0], repeat_probs)

    axs[1].set_title('Model Based')
    plot_MB_probs(axs[1], repeat_probs)

    plt.show()


def plot_window_repeat_probs(repeat_probs, window_size, diff, subject_ID):

    fig, axs = plt.subplots(5, 8)
    fig.suptitle('Subject#{}'.format(int(subject_ID)))

    for i, start in enumerate(range(0, N_TRIALS-window_size, diff)):
        for j, key in enumerate(['model_free', 'model_based']):

            row, col = int(i/4), (i%4)*2+j

            if key == 'model_free':
                axs[row, col].set_title('MF: Trials {}:{}'.format(start, start+window_size))
                plot_MF_probs(axs[row, col], repeat_probs, start, window_size)
            else:
                axs[row, col].set_title('MB: Trials {}:{}'.format(start, start+window_size))
                plot_MB_probs(axs[row, col], repeat_probs, start, window_size)

    plt.show()


def plot_subject_single_coef(coefficients, x_labels, axs, model_label, coeff_name):

    xs = [i for i, _ in enumerate(x_labels)]
    ys = [coefficients[model_label][x_label][coeff_name] for x_label in x_labels]
    axs.plot(xs, ys, label='window\'s coefficient')
    main_y = [coefficients[model_label][(0, N_TRIALS)][coeff_name] for y in ys]
    axs.plot(xs, main_y, label='final coefficient')
    axs.set_xticks(range(len(xs)))
    axs.set_xticklabels(x_labels, rotation=45)
    axs.set_title('{}: {}\'s coeff'.format(model_label.replace('_', '-'), coeff_name).replace('_', ' '))
    axs.legend()


def plot_subject_windows_all_coefs(coefficients, window_size, diff, subject_ID):

    fig, axs = plt.subplots(3, 2)
    fig.suptitle('Subject#{}'.format(int(subject_ID)))
    fig.tight_layout()
    x_labels = [(i, i+window_size) for i in range(0, N_TRIALS-window_size, diff)]

    for i, mf_coeff_name in enumerate(['common_reward', 'unique_reward', 'interaction']):
        plot_subject_single_coef(coefficients, x_labels, axs[i, 0], 'model_free', mf_coeff_name)
    for i, mb_coeff_name in enumerate(['common_reward', 'reward_prob', 'interaction']):
        plot_subject_single_coef(coefficients, x_labels, axs[i, 1], 'model_based', mb_coeff_name)

    plt.show()


def plot_differece_means(differences_data, window_size, diff):

    x_labels = [(i, i+window_size) for i in range(0, N_TRIALS-window_size, diff)]
    xs = [i for i, _ in enumerate(x_labels)]
    fig, axs = plt.subplots(3, 2)
    fig.tight_layout()

    for i, model_key in enumerate(differences_data.keys()):
        for j, coef in enumerate(differences_data[model_key].keys()):
            ys = [differences_data[model_key][coef][x_label]['mean'] for x_label in x_labels]
            errors = [differences_data[model_key][coef][x_label]['se'] for x_label in x_labels]

            axs[j, i].errorbar(xs, ys, yerr=errors, fmt='o')
            axs[j, i].plot(xs, [0 for x in xs], label='zero line')
            axs[j, i].set_xticks(range(len(xs)))
            axs[j, i].set_xticklabels(x_labels, rotation=45)
            axs[j, i].set_title('{}: {} coef\'s difference from main coef'\
                .format(model_key.replace('_', '-'), coef.replace('_', ' ')))
            axs[j, i].legend()

    plt.show()
