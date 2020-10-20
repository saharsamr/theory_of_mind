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
