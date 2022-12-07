# -*- coding: utf-8 -*-
from os import path

import aiofiles
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from database import Database, Column
from mounts import student, mark, subject, teacher, group
from docs.autodocs import AutoDocs

from config import DB_NAME


app = FastAPI(
    version='0.0.7',  # 0 algorithms, 0 features, 7 bugs
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
app.mount('/group', group)

DOCS_FILE = './docs/index.html'
AutoDocs.generate(
    root='./docs/',
    title='Mark_System::Docs',
    models=[
        ('Group', '../database/types/group.py'),
        ('Mark', '../database/types/mark.py'),
        ('Student', '../database/types/student.py'),
        ('Subject', '../database/types/subject.py'),
        ('Teacher', '../database/types/teacher.py'),
        ('User', '../database/types/user.py'),
        ('AdminPayloadModel', '../models/__init__.py'),
    ],
    methods=[
        ('group', '../mounts/group.py'),
        ('mark', '../mounts/mark.py'),
        ('student', '../mounts/student.py'),
        ('subject', '../mounts/subject.py'),
        ('teacher', '../mounts/teacher.py'),
    ],
    exceptions=[
        '../exceptions.py'
    ],
    tailwind_colors={
        'back': '#080f11',
        'fore': '#49c491',
        'code-back': '#acacac',
        'back-light': '#7ac499',
        'fore-light': '#57c4ba',
    },
    thumb_color='#49c491'
)


@app.get('/docs')
async def get_api_doc():
    if path.exists(DOCS_FILE) and path.isfile(DOCS_FILE):
        async with aiofiles.open(DOCS_FILE, 'r', encoding='utf-8') as f:
            content = await f.read()
        return HTMLResponse(content=content)
    return JSONResponse(
        content={'error': 'not found'},
        status_code=status.HTTP_404_NOT_FOUND
    )


@app.get('/docs/{folder}/{file}')
async def get_api_doc(folder: str, file: str):
    file = f'./docs/{folder}/{file}'
    if path.exists(file) and path.isfile(file):
        return FileResponse(path=file)
    return JSONResponse(
        content={'error': 'not found'},
        status_code=status.HTTP_404_NOT_FOUND
    )

db = Database(DB_NAME)


def main():
    db.create_table(
        'mark',
        Column('m_id', Column.Type.INT, primary_key=True, autoincrement=True),
        Column('score', Column.Type.INT),
        Column('title', Column.Type.TEXT),
        Column('subject_id', Column.Type.INT),
        Column('student_id', Column.Type.INT),
        Column('date', Column.Type.INT),
    ).if_not_exists().also().create_table(
            'student',
            Column('s_id', Column.Type.INT, primary_key=True, autoincrement=True),
            Column('name', Column.Type.TEXT),
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
            Column('access_token', Column.Type.TEXT),
            Column('email', Column.Type.TEXT),
            Column('password', Column.Type.TEXT),
        ).if_not_exists().also().create_table(
            'studentGroup',
            Column('group_id', Column.Type.INT, primary_key=True, autoincrement=True),
            Column('name', Column.Type.TEXT),
        ).if_not_exists().execute()


main()
