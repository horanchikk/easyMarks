# -*- coding: utf-8 -*-
from .. import DatabaseType


class Subject(DatabaseType):
    template = ['s_id', 'title', 'teacher_id', 'students']

    s_id: int
    title: str
    teacher_id: int
    students: list[int]

    def __init__(self, *args):
        super().__init__(*args)
        self.students = [int(i) for i in self.students.split(',')]
