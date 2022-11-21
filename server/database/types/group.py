# -*- coding: utf-8 -*-
from ..dbtype import DatabaseType


class Group(DatabaseType):
    template = ['group_id', 'name']

    group_id: int
    name: str

    def __repr__(self):
        return f'[{self.group_id}] {self.name}'
