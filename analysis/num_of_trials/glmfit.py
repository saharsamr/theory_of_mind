import statsmodels.api as sm
from patsy import dmatrices


def fit_binomial_glm(subject_data, formula):

    y, x = dmatrices(formula, subject_data, return_type='dataframe')
    MF_model = sm.GLM(y, x, family=sm.families.Binomial())
    MF_result = MF_model.fit()

    return MF_model, MF_result
