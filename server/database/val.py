# -*- coding: utf-8 -*-
from .util import _to_sql_value


class Val:
    def __init__(
            self,
            name: str,
            value: str
    ):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.name} = {_to_sql_value(self.value)}'
