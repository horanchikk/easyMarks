# -*- coding: utf-8 -*-
from fastapi import FastAPI

from config import ADMIN_TOKEN, DB_NAME
from database import Database
from database.types.teacher import Teacher
from exceptions import HttpError
from models import AdminPayloadModel

teacher = FastAPI(redoc_url=None, docs_url=None)

db = Database(DB_NAME)


@teacher.post('/')
async def create_teacher(
        name: str,
        email: str,
        password: str,
        payload: AdminPayloadModel
):
    """Создание преподавателя

    :param name: ФИО преподавателя
    :param email: E-mail преподавателя
    :param password: пароль
    :param payload: полезная нагрузка
    """
    if payload.admin_token != ADMIN_TOKEN:
        return HttpError.ADMIN_ACCESS_REQUIRE
    last_id = db.insert_one('teacher', 'name', 'access_token', 'email', 'password').values(
        name, Teacher.new_token(), email, password
    ).exec()
    return {
        'response': last_id
    }
