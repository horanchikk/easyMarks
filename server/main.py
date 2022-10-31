# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Database, Column
from mounts import student, mark, subject, teacher

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
app.mount('/mark', mark)
app.mount('/subject', subject)
app.mount('/teacher', teacher)

db = Database(DB_NAME)


def main():
    db.create_table(
        'mark',
        Column('m_id', Column.Type.INT, primary_key=True, autoincrement=True),
        Column('score', Column.Type.INT),
        Column('title', Column.Type.TEXT),
        Column('subject_id', Column.Type.INT),
        Column('date', Column.Type.INT),
    ).if_not_exists().also().create_table(
            'student',
            Column('s_id', Column.Type.INT, primary_key=True, autoincrement=True),
            Column('name', Column.Type.TEXT),
            Column('subjects', Column.Type.TEXT),
            Column('group_id', Column.Type.INT),
        ).if_not_exists().also().create_table(
            'subject',
            Column('s_id', Column.Type.INT, primary_key=True, autoincrement=True),
            Column('title', Column.Type.TEXT),
            Column('teacher_id', Column.Type.INT),
            Column('groups', Column.Type.TEXT),
        ).if_not_exists().also().create_table(
            'teacher',
            Column('teacher_id', Column.Type.INT, primary_key=True, autoincrement=True),
            Column('name', Column.Type.TEXT),
            Column('subjects_ids', Column.Type.TEXT),
            Column('access_token', Column.Type.TEXT),
        ).if_not_exists().exec()


main()
