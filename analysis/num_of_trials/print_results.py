from tools.print_table import print_table


N_TRIALS = 300


def print_glm_results(mf_result, mb_result):

    print('======================================================================================')
    print('--------------------------------------Model-Free--------------------------------------')
    print('======================================================================================')
    print(mf_result.summary())
    print('======================================================================================')
    print('--------------------------------------Model-Based--------------------------------------')
    print('======================================================================================')
    print(mb_result.summary())


def print_windows_ttest_results(t_test_results, window_size, diff):

    for model_key in t_test_results.keys():
        for coef in t_test_results[model_key].keys():

            field_names, statistic, pvalue = [''], ['statistic'], ['pvalue']
            print('***********************************{}: {}'.format(model_key.replace('_', '-'), coef.replace('_', ' ')))
            for start in range(0, N_TRIALS-window_size, 2*diff):
                stats = t_test_results[model_key][coef][(start, start+window_size)]
                field_names.append((start, start+window_size))
                statistic.append(int(stats['statistic']*1000)/1000)
                pvalue.append(int(stats['pvalue']*1000)/1000)
            print_table(field_names, [statistic, pvalue])
