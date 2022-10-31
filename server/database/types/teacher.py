# -*- coding: utf-8 -*-
from secrets import token_hex

from .. import DatabaseType


class Teacher(DatabaseType):
    template = ['teacher_id', 'name', 'subjects_ids', 'access_token']

    teacher_id: int
    name: str
    subjects_ids: list[int]
    access_token: str

    def __init__(self, *args):
        super().__init__(*args)
        self.subjects_ids = [int(i) for i in self.subjects_ids.split(',')]

    @staticmethod
    def new_token():
        return f'marksystem:v1:{token_hex(32)}'
