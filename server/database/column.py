# -*- coding: utf-8 -*-
from enum import Enum


class Column:
    class Type(Enum):
        INT = 'INTEGER'
        TEXT = 'TEXT'
        REAL = 'REAL'
        BLOB = 'BLOB'

    def __init__(
            self,
            name: str,
            column_type: str | Type,
            primary_key: bool = False,
            autoincrement: bool = False,
            not_null: bool = True
    ):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.not_null = not_null

    def __str__(self) -> str:
        if isinstance(self.column_type, Column.Type):
            result = f'{self.name} {self.column_type.value}'
        else:
            result = f'{self.name} {self.column_type}'
        if self.primary_key:
            result += ' PRIMARY KEY'
            if self.autoincrement:
                result += ' AUTOINCREMENT'
        if self.not_null:
            result += ' NOT NULL'
        return result
