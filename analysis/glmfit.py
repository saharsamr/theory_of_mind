import statsmodels.api as sm
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
from patsy import dmatrices


def fit_binomial_glm(subject_data, formula):

    y, x = dmatrices(formula, subject_data, return_type='dataframe')
    MF_model = sm.GLM(y, x, family=sm.families.Binomial())
    MF_result = MF_model.fit()

    return MF_model, MF_result


def fit_mixed_lm(subjects_data, formula, random_factors_formulas=None):

    model = BinomialBayesMixedGLM.from_formula(formula, random_factors_formulas, subjects_data)
    result = model.fit_vb()

    return model, result
