from tools.directory_files import get_file_names
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

        file_names = get_file_names(TaskParams.data_dir, 'csv')
        if file_names:
            subject_ids = [int(f.replace('.csv', ''))]
            return max(subject_ids) + 1
        else:
            return 1
