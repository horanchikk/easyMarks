# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, Column, Val
from database.types.subject import Subject
from config import DB_NAME, ADMIN_TOKEN
from exceptions import HttpError
from models import AdminPayloadModel

subject = FastAPI(redoc_url=None, docs_url=None)

db = Database(DB_NAME)


@subject.get('/id{subject_id}')
async def get_subject(subject_id: int):
    """Получает предмет по ID

    :param subject_id: ID предмета
    """
    s = db.select('subject').where(Val('s_id', subject_id)).fetch_one_to(Subject)
    return { 'response': s.dict() }


@subject.post('/')
async def create_subject(
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
