import scipy.io as io


def load_mat(path):

    mat = io.loadmat(path, mat_dtype=True, struct_as_record=True)
    return mat
