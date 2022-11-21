# -*- coding: utf-8 -*-
from secrets import token_hex

from .. import DatabaseType


class Teacher(DatabaseType):
    template = ['teacher_id', 'name', 'access_token', 'email', 'password']

    teacher_id: int
    name: str
    access_token: str
    email: str
    password: str

    @staticmethod
    def new_token():
        return f'marksystem:v1:{token_hex(32)}'
