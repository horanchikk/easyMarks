# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, Val
from database.types.student import Student
from config import DB_NAME, ADMIN_TOKEN
from exceptions import HttpError
from models import AdminPayloadModel

student = FastAPI(docs_url=None, redoc_url=None)
db = Database(DB_NAME)['student']


@student.get('/id{student_id}')
async def student_get_by_id(student_id: int):
    """Получить студента по ID

    :param student_id: ID студента
    """
    result = db.select().where(Val('s_id', student_id)).fetch_one_to(Student)
    return {
        'response': result.dict()
    }


@student.get('/group{group_id}')
async def student_get_by_group(group_id: int):
    """Получить группу по ID

    :param group_id: ID группы
    """
    result = db.select().where(Val('group_id', group_id)).fetch_to(Student)
    return {
        'response': {
            'items': [i.dict() for i in result],
            'size': len(result)
        }
    }


@student.post('/')
async def student_create(
        name: str,
        group_id: int,
        payload: AdminPayloadModel
):
    """Создание студента

    :param name: ФИО студента
    :param group_id: ID группы
    :param payload: полезная нагрузка
    """
    if payload.admin_token != ADMIN_TOKEN:
        return HttpError.ADMIN_ACCESS_REQUIRE
    last_id = db.insert_one('student', 'name', 'group_id').values(
        name, group_id
    ).exec()
    return {
        'response': last_id
    }
