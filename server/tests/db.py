# -*- coding: utf-8- -*-
from unittest import TestCase, main
from database import Database, Column, Val
from database.types.user import User


class DBTest(TestCase):
    db = Database('test.db')

    def test_00_create_table_if_not_exists(self):
        self.db.create_table(
            'testDb',
            Column('id', Column.Type.INT, primary_key=True),
            Column('name', Column.Type.TEXT),
        ).if_not_exists().exec()
        self.db.insert_one('testDb', 'name').values('Вадим гей').exec()
        self.db.insert_one('testDb', 'name').values('Никита гей').exec()
        self.db.insert_one('testDb', 'name').values('Никита гей 1 ').exec()
        self.db.insert_one('testDb', 'name').values('Никита гей 2').exec()
        self.db.insert_one('testDb', 'name').values('Никита гей3 ').exec()
        self.db.update_one('testDb').set(
            Val('name', 'Вадим не гей')
        ).where(Val('id', 1)).exec()

    def test_01_select_order_by(self):
        print(self.db.select('testDb').where(Val('id', 1)).fetch())
        print(self.db.select('testDb').fetch())
        print(self.db.select('testDb').limit(5).fetch())
        print(self.db.select('testDb').order_by('name').limit(5).fetch())
        print(self.db.select('testDb').order_by('name', True).limit(5).fetch())

    def test_02_typing(self):
        users: list[User] = self.db.select('testDb').where(Val('id', 1)).fetch_to(User)
        print(users[0].name)

        users = self.db.select('testDb').limit(10).fetch_to(User)
        print(users)
        print([i.uid for i in users])

    def test_03_rowcount(self):
        print(self.db.row_count('testDb'))


if __name__ == '__main__':
    main(verbosity=2)
    pass
