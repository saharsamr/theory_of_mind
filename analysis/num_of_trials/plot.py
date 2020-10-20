import matplotlib.pyplot as plt
import numpy as np


N_TRIALS = 300


def plot_whole_repeat_probs(repeat_probs, subject_ID):
    fig, axs = plt.subplots(1, 2)
    fig.suptitle('Subject#{}'.format(int(subject_ID)))

    axs[0].set_title('Model Free')
    xs = [0, 1]
    probs = repeat_probs['model_free'][(0, N_TRIALS)]
    ys = [probs['common1_unique0'], probs['common1_unique1']]
    axs[0].plot(xs, ys, label='common = 1')
    ys = [probs['common0_unique0'], probs['common0_unique1']]
    axs[0].plot(xs, ys, label='common = 0')
    axs[0].set_xticks(range(2))
    axs[0].set_xticklabels(['U=0', 'U=1'])
    axs[0].set_ylim([0, 1])
    axs[0].legend()

    axs[1].set_title('Model Based')
    xs = [0, 1]
    probs = repeat_probs['model_based'][(0, N_TRIALS)]
    ys = [probs['common0'], probs['common1']]
    axs[1].plot(xs, ys)
    axs[1].set_xticks(range(2))
    axs[1].set_xticklabels(['C=0', 'C=1'])
    axs[1].set_ylim([0, 1])

    plt.show()


def plot_sub_repeat_probs(repeat_probs, window_size, diff, subject_ID):

    fig, axs = plt.subplots(5, 8)
    fig.suptitle('Subject#{}'.format(int(subject_ID)))
    for i, start in enumerate(range(0, N_TRIALS-window_size, diff)):
        for j, key in enumerate(['model_free', 'model_based']):
            row, col = int(i/4), (i%4)*2+j
            if key == 'model_free':
                axs[row, col].set_title('MF: Trials {}:{}'.format(start, start+window_size))

                xs = [0, 1]
                probs = repeat_probs[key][(start, start+window_size)]
                ys = [probs['common1_unique0'], probs['common1_unique1']]
                axs[row, col].plot(xs, ys, label='common = 1')
                ys = [probs['common0_unique0'], probs['common0_unique1']]
                axs[row, col].plot(xs, ys, label='common = 0')

                axs[row, col].set_xticks(range(2))
                axs[row, col].set_xticklabels(['U=0', 'U=1'])
                axs[row, col].legend()
            else:
                axs[row, col].set_title('MB: Trials {}:{}'.format(start, start+window_size))

                xs = [0, 1]
                probs = repeat_probs[key][(start, start+window_size)]
                ys = [probs['common0'], probs['common1']]
                axs[row, col].plot(xs, ys)

                axs[row, col].set_xticks(range(2))
                axs[row, col].set_xticklabels(['C=0', 'C=1'])

            axs[row, col].set_ylim([0, 1])

    plt.show()
