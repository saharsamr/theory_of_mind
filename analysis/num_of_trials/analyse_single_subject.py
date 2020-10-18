from analysis.num_of_trials.extract_info import extract_subject_trials_info
from analysis.num_of_trials.glmfit import fit_binomial_glm


N_TRIALS = 300


def analyse_trials(subject_filtered_data, start_index=0):

    model_free_data, model_based_data = extract_subject_trials_info(subject_filtered_data, start_index)
    print('*** model free part')
    mf_model, mf_result = fit_binomial_glm(model_free_data, formula='repeat ~ common_reward*unique_reward')
    print('*** model based part')
    mb_model, mb_result = fit_binomial_glm(model_based_data, formula='repeat ~ common_reward*reward_prob')


def get_trials_subset(subject_filtered_data, start_index, end_index):

    result = {
        'chosen': subject_filtered_data['chosen'][start_index:end_index],
        'realized_reward': subject_filtered_data['realized_reward'][start_index:end_index],
        'outcome': subject_filtered_data['outcome'],
        'trials': subject_filtered_data['trials'][start_index:end_index],
        'reward_probs': subject_filtered_data['reward_probs'][start_index:end_index]
    }
    return result


def analyse_with_moving_window(subject_filtered_data, window_size, diff):

    for start in range(0, N_TRIALS-window_size, diff):
        subset_filtered_data = get_trials_subset(subject_filtered_data, start, start+window_size)
        print('####### From {} to {} #######'.format(start, start+window_size))
        analyse_trials(subset_filtered_data, start_index=start)


def analyse_single_subject(subject_filtered_data, subject_ID, window_size, diff):

    print('Subject ID: {}'.format(subject_ID))

    print('####### On Whole Trials #######')
    analyse_trials(subject_filtered_data)

    analyse_with_moving_window(subject_filtered_data, window_size, diff)
