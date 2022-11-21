# -*- coding: utf-8 -*-
from .. import DatabaseType


class Student(DatabaseType):
    template = ['s_id', 'name', 'group_id']

    s_id: int
    name: str
    group_id: int
