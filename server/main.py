# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Database, Column, Val
from mounts import student

from config import DB_NAME


app = FastAPI(
    version='0.0.1',
    docs_url=None,
    redoc_url=None
)
app.add_middleware(
    CORSMiddleware,
    allow_headers=['*'],
    allow_methods=['*'],
    allow_origins=['*']
)
app.mount('/student', student)

db = Database(DB_NAME)


def main():
    db.create_table(
        'mark',
        Column('m_id', Column.Type.INT, primary_key=True, autoincrement=True),
        Column('score', Column.Type.INT),
        Column('title', Column.Type.TEXT),
        Column('subject_id', Column.Type.INT),
        Column('date', Column.Type.INT),
    ).if_not_exists().exec()
    db.create_table(
        'student',
        Column('s_id', Column.Type.INT, primary_key=True, autoincrement=True),
        Column('name', Column.Type.TEXT),
        Column('subjects', Column.Type.TEXT),
        Column('group_id', Column.Type.INT),
    ).if_not_exists().exec()

    db.insert_one('student', 'name', 'subjects', 'group_id').values(
        'Кирилл Рыжов', '1,2,3', 1
    ).exec()


main()
