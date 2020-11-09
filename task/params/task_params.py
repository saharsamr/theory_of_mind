class TaskParams:

    data_dir = 'task/data/'
    image_dir = 'task/images/'
    instructions_path = 'task/instructions/'

    first_options = (1, 2, 3, 4)
    second_options = (1, 2, 3, 4)
    objects = (11, 12, 13, 14)

    options_pairs = None


    @classmethod
    def set_options_pairs(cls, pairs):

        cls.options_pairs = pairs
