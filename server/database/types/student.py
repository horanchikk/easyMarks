# -*- coding: utf-8 -*-
from .. import DatabaseType


class Student(DatabaseType):
    template = ['s_id', 'name', 'subjects', 'group_id']

    s_id: int
    name: str
    subjects: list[int]
    group_id: int

    def __init__(self, *args):
        super().__init__(*args)
        self.subjects = [int(i) for i in self.subjects.split(',')]
