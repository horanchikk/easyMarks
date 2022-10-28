# -*- coding: utf-8 -*-
from .. import DatabaseType


class Subject(DatabaseType):
    template = ['s_id', 'title', 'teacher_id', 'groups']

    s_id: int
    title: str
    teacher_id: int
    groups: list[int]

    def __init__(self, *args):
        super().__init__(*args)
        self.groups = [int(i) for i in self.groups.split(',')]
