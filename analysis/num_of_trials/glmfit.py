import statsmodels.api as sm
from patsy import dmatrices


def clean_MFdata_for_glm(common_reward_MF, unique_reward_MF, repeat_MF):

    data = np.empty((len(common_reward_MF), 3))
    for i, (common_reward, unique_reward, repeat) in enumerate(zip(common_reward_MF, unique_reward_MF, repeat_MF)):

        data[i][0] = common_reward
        data[i][1] = unique_reward
        data[i][2] = repeat

    df = pd.DataFrame(data, columns=['common_reward', 'unique_reward', 'repeat'])
    df = df.astype(dtype={'common_reward': 'int64', 'unique_reward': 'int64', 'repeat': 'int64'})

    return df


def clean_MBdata_for_glm(common_reward_MB, reward_prob_MB, repeat_MB):

    data = np.empty((len(common_reward_MB), 3))
    for i, (common_reward, reward_prob, repeat) in enumerate(zip(common_reward_MB, reward_prob_MB, repeat_MB)):

        data[i][0] = common_reward
        data[i][1] = reward_prob
        data[i][2] = repeat

    df = pd.DataFrame(data, columns=['common_reward', 'reward_prob', 'repeat'])
    df = df.astype(dtype={'common_reward': 'int64', 'reward_prob': 'float64', 'repeat': 'int64'})

    return df


def fit_glm_MF(subject_data):

    MF_formula = 'repeat ~ common_reward*unique_reward'
    y, x = dmatrices(MF_formula, subject_data, return_type='dataframe')
    MF_model = sm.GLM(y, x, family=sm.families.Binomial())
    MF_result = MF_model.fit()

    print(MF_result.summary())


def fit_glm_MB(subject_data):

    MB_formula = 'repeat ~ common_reward*reward_prob'
    y, x = dmatrices(MB_formula, subject_data, return_type='dataframe')
    MB_model = sm.GLM(y, x, family=sm.families.Binomial())
    MB_result = MB_model.fit()

    print(MB_result.summary())
