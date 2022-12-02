# -*- coding: utf-8 -*-
import time

from fastapi import FastAPI

from database import Database, Val
from database.types.mark import Mark
from config import DB_NAME
from database.types.student import Student
from database.types.subject import Subject
from database.types.teacher import Teacher
from exceptions import HttpError

mark = FastAPI(redoc_url=None, docs_url=None)
db = Database(DB_NAME)['mark']


@mark.get('/id{m_id}')
async def get_mark_by_id(m_id: int):
    """Получить оценку по ID

    :param m_id: ID оценки
    """
    result = db.select().where(Val('m_id', m_id)).fetch_one_to(Mark)
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
    """Поставить оценку студенту

    :param student_id: ID студента
    :param subject_id: ID предмета
    :param title: за что оценка
    :param score: оценка
    :param access_token: токен преподавателя
    """
    teacher = db.select('teacher').where(Val('access_token', access_token)).fetch_one_to(Teacher)
    if teacher is None:
        return HttpError.WRONG_ACCESS_TOKEN
    subject = db.select('subject').where(Val('s_id', subject_id)).fetch_one_to(Subject)
    if subject is None:
        return HttpError.INVALID_SUBJECT_ID
    if teacher.teacher_id != subject.teacher_id:
        return HttpError.NOT_ACCESS_TO_THIS_SUBJECT
    student = db.select('student').where(Val('s_id', student_id)).fetch_one_to(Student)
    if student is None:
        return HttpError.INVALID_STUDENT_ID
    if student.group_id not in subject.groups:
        return HttpError.THIS_STUDENT_HAS_NT_SBJ
    db.insert_one('mark', 'score', 'title', 'subject_id', 'student_id', 'date').values(
        score, title, subject_id, student_id, time.time()
    )
    return {
        'response': db.exec()
    }
