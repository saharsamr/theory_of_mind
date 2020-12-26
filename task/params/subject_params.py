from tools.directory_files import get_directory_names, get_file_names
from task.params.task_params import TaskParams

import datetime
import random


class SubjectParams:

    subject_date = datetime.datetime.now()
    subject_id = None
    subject_age = None
    subject_gender = None
    phases_random_walks = None


    @classmethod
    def set_subject_info(cls, subject_info):

        cls.subject_id = cls._find_new_subject_id_()
        cls.subject_age = subject_info['age']
        cls.subject_gender = subject_info['gender']
        cls._select_random_walks_()


    @staticmethod
    def _find_new_subject_id_():

        dir_names = get_directory_names(TaskParams.data_dir)
        if dir_names:
            subject_ids = [int(name) for name in dir_names]
            return max(subject_ids) + 1
        else:
            return 1


    @classmethod
    def _select_random_walks_(cls):

        file_names = get_file_names(TaskParams.random_walks_path, 'pkl')
        file_names = [name.replace('walk', '') for name in file_names]
        file_names = [name.replace('.pkl', '') for name in file_names]
        selected_random_walks = random.sample(file_names, 3)
        cls.phases_random_walks = [int(selected) for selected in selected_random_walks]
