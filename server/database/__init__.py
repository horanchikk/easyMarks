# -*- coding: utf-8 -*-
from sqlite3 import connect

from .column import Column
from .val import Val
from .util import _to_sql_value
from .dbtype import DatabaseType


class Database:
    def __init__(
            self,
            db_name: str = 'data.db'
    ):
        """Initializes database

        :param db_name: название файла для подключения
        """
        if not db_name.endswith('.db'):
            db_name += '.db'
        self.con = connect(db_name)
        self.cur = self.con.cursor()
        self.query = ''

    def also(self) -> 'Database':
        self.query += ';'
        return self

    def clear_query(self):
        """Clears query"""
        self.query = ''

    def row_count(self, table: str) -> int:
        """Returns table length"""
        return len(self.cur.execute(f'SELECT * FROM {table}').fetchall())

    def create_table(
            self,
            name: str,
            *columns: Column
    ) -> 'Database':
        """Creates table with specified columns

        :param name: table name
        :param columns: list of Column objects
        """
        data = ','.join([str(i) for i in columns])
        self.query += f'CREATE TABLE {name} ({data})'
        return self

    def execute(self) -> 'Database':
        """Executes query by cursor"""
        if ';' in self.query:
            self.cur.executescript(self.query)
        else:
            self.cur.execute(self.query)
        self.clear_query()
        return self

    def commit(self) -> 'Database':
        """Commits all changes of cursor"""
        self.con.commit()
        return self

    def exec(self) -> int:
        """Executes and commits"""
        print(self.query)
        self.execute()
        self.commit()
        return self.cur.lastrowid

    def insert_one(self, table: str, *columns: str) -> 'Database':
        """Insert one row into table

        :param table: table name
        :param columns: column names
        """
        self.query += f'INSERT INTO {table} ({",".join(columns)})'
        return self

    def update_one(self, table: str) -> 'Database':
        """Updates one row"""
        self.query += f'UPDATE {table}'
        return self

    def values(self, *values: str) -> 'Database':
        """Specifies values for inserting

        :param values: values
        """
        self.query += f' VALUES({",".join([_to_sql_value(i) for i in values])})'
        return self

    def if_not_exists(self) -> 'Database':
        """Adds IF NOT EXISTS into query"""
        splitted = self.query.split(';')
        splitted[-1] = splitted[-1].replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
        self.query = ';'.join(splitted)
        return self

    def set(self, *values: Val) -> 'Database':
        """Adds where syntax to query"""
        self.query += f' SET {",".join(str(i) for i in values)}'
        return self

    def select(self, table: str) -> 'Database':
        """Select from table

        :param table: table name
        """
        self.query += f" SELECT * FROM {table}"
        return self

    def where(self, *values: Val) -> 'Database':
        """Adds where syntax to query"""
        self.query += f' WHERE {",".join(str(i) for i in values)}'
        return self

    def limit(self, count: int, offset: int = 0) -> 'Database':
        """Adds limit into query

        :param count: limit of query
        :param offset: offset rows
        """
        self.query += f' LIMIT {offset},{count}'
        return self

    def order_by(self, column_name: str, reverse: bool = False) -> 'Database':
        """Adds order by into query

        :param column_name: column name
        :param reverse: use reverse sorting
        """
        self.query += f' ORDER BY {column_name} {"DESC" if reverse else "ASC"}'
        return self

    def fetch(self) -> list:
        result = self.cur.execute(self.query).fetchall()
        self.clear_query()
        return result

    def fetch_one(self):
        result = self.cur.execute(self.query).fetchone()
        self.clear_query()
        return result

    def fetch_to(self, typed):
        return self.to(self.fetch(), typed)

    def fetch_one_to(self, typed):
        return self.to(self.fetch_one(), typed)

    def to(self, value: tuple | list, typed):
        if value is None:
            return None
        if isinstance(value, list):
            return [typed(*i) for i in value]
        return typed(*value)
