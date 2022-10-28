# -*- coding: utf-8 -*-
from .. import DatabaseType


class Teacher(DatabaseType):
    template = ['teacher_id', 'name', 'subjects_ids']

    teacher_id: int
    name: str
    subjects_ids: list[int]

    def __init__(self, *args):
        super().__init__(*args)
        self.subjects_ids = [int(i) for i in self.subjects_ids.split(',')]
