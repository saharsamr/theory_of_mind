class TaskParams:

    data_dir = 'task/data/'
    image_dir = 'task/images/'
    instructions_path = 'task/instructions/'

    first_options = (0, 1, 2, 3)
    second_options = (0, 1, 2, 3)
    objects = (10, 11, 12, 13)

    options_pairs = None
    objects_of_options = None


    @classmethod
    def set_options_pairs(cls, pairs):
        cls.options_pairs = pairs


    @classmethod
    def set_objects_of_options(cls, objects_of_options):
        cls.objects_of_options = objects_of_options
