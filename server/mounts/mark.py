# -*- coding: utf-8 -*-
import time

from fastapi import FastAPI

from database import Database, Val
from database.types.mark import Mark
from config import DB_NAME
from database.types.student import Student
from database.types.subject import Subject
from database.types.teacher import Teacher

mark = FastAPI(redoc_url=None, docs_url=None)
db = Database(DB_NAME)


@mark.get('/id{m_id}')
async def get_mark_by_id(m_id: int):
    """Finds mark by its ID"""
    result = db.select('mark').where(Val('m_id', m_id)).fetch_one_to(Mark)
    return {
        'response': result.dict()
    }


@mark.post('/')
async def add_mark(
        student_id: int,
        subject_id: int,
        title: str,
        score: int,
        access_token: str
):
    """Adds mark to one student

    :param student_id: student ID
    :param subject_id: subject ID
    :param title: mark title
    :param score: mark score
    :param access_token: teacher's access token
    """
    teacher = db.select('teacher').where(Val('access_token', access_token)).fetch_one_to(Teacher)
    if teacher is None:
        return {'error': 'wrong access token'}
    subject = db.select('subject').where(Val('s_id', subject_id)).fetch_one_to(Subject)
    if subject is None:
        return {'error': 'invalid subject ID'}
    if teacher.teacher_id != subject.teacher_id:
        return {'error': 'You have not access to this subject'}
    student = db.select('student').where(Val('s_id', student_id)).fetch_one_to(Student)
    if student is None:
        return {'error': 'invalid student ID'}
    if student.group_id not in subject.groups:
        return {'error': 'this student has not this subject'}
    db.insert_one('mark', 'score', 'title', 'subject_id', 'student_id', 'date').values(
        score, title, subject_id, student_id, time.time()
    )
    return {
        'response': db.exec()
    }
