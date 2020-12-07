from tools.directory_files import get_directory_names
from task.params.task_params import TaskParams

import datetime


class SubjectParams:

    subject_date = datetime.datetime.now()
    subject_id = None
    subject_age = None
    subject_gender = None


    @classmethod
    def set_subject_info(cls, subject_info):

        cls.subject_id = cls._find_new_subject_id_()
        cls.subject_age = subject_info['age']
        cls.subject_gender = subject_info['gender']


    @staticmethod
    def _find_new_subject_id_():

        dir_names = get_directory_names(TaskParams.data_dir)
        print(dir_names)
        if dir_names:
            subject_ids = [int(name) for name in dir_names]
            return max(subject_ids) + 1
        else:
            return 1
