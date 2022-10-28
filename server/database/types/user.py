# -*- coding: utf-8 -*-
from ..dbtype import DatabaseType


class User(DatabaseType):
    template = ['uid', 'name']
    uid: int
    name: str

    def __repr__(self):
        return f'[{self.uid}] {self.name}'
