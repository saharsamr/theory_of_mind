from tools.print_table import print_table


N_TRIALS = 300


def print_windows_ttest_results(t_test_results, window_size, diff):

    for model_key in t_test_results.keys():
        for coef in t_test_results[model_key].keys():

            field_names, statistic, pvalue = [''], ['statistic'], ['pvalue']
            for start in range(0, N_TRIALS-window_size, 2*diff):
                stats = t_test_results[model_key][coef][(start, start+window_size)]
                field_names.append((start, start+window_size))
                statistic.append(int(stats['statistic']*1000)/1000)
                pvalue.append(int(stats['pvalue']*1000)/1000)
            print_table(field_names, [statistic, pvalue])
