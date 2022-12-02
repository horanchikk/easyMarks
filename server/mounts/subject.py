# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, Val
from database.types.group import Group
from database.types.mark import Mark
from database.types.student import Student
from database.types.subject import Subject
from config import DB_NAME, ADMIN_TOKEN
from exceptions import HttpError
from models import AdminPayloadModel

subject = FastAPI(redoc_url=None, docs_url=None)

db = Database(DB_NAME)['subject']


@subject.get('/id{subject_id}')
async def subject_by_id(subject_id: int):
    """Получает предмет по ID

    :param subject_id: ID предмета
    """
    s = db.select().where(Val('s_id', subject_id)).fetch_one_to(Subject)
    return {'response': s.dict()}


@subject.get('/marks{subject_id}:{group_id}')
async def subject_get_marks(subject_id: int, group_id: int):
    """Получение всех оценок по предмету и группе

    :param subject_id: ID предмета
    :param group_id: ID группы
    """
    subj: Subject = db.select().where(Val('s_id', subject_id)).fetch_one_to(Subject)
    if subj is None:
        return HttpError.INVALID_SUBJECT_ID
    g: Group = db.select('group').where(Val('group_id', group_id)).fetch_one_to(Group)
    if g is None:
        return HttpError.INVALID_GROUP_ID
    students: list[Student] = db.select('student').where(Val('group', g.group_id)).fetch_to(Student)
    marks: dict[Mark] = []
    for s in students:
        _marks: list[Mark] = db.select('mark').where(
            Val('student_id', s.s_id), Val('subject_id', subject_id)
        ).fetch_to(Mark)
        marks[s.s_id] = [{
            'id': i.m_id,
            'score': i.score,
            'title': i.title,
            'timestamp': i.date
        } for i in _marks]
    return {
        'response': marks
    }


@subject.post('/')
async def subject_create(
        title: str,
        teacher_id: int,
        groups: str,
        payload: AdminPayloadModel
):
    """Создание предмета

    :param title: название предмета
    :param teacher_id: ID преподавателя
    :param groups: список ID групп через запятую
    :param payload: полезная нагрузка
    """
    if payload.admin_token != ADMIN_TOKEN:
        return HttpError.ADMIN_ACCESS_REQUIRE
    last_id = db.insert_one(
        'subject', 'title', 'teacher_id', 'groups'
    ).values(title, teacher_id, groups).exec()
    return {
        'response': last_id
    }
