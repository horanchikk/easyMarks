# -*- coding: utf-8 -*-
from fastapi import FastAPI
from werkzeug.security import check_password_hash, generate_password_hash

from config import ADMIN_TOKEN, DB_NAME
from database import Database, Val
from database.types.teacher import Teacher
from exceptions import HttpError
from models import AdminPayloadModel

teacher = FastAPI(redoc_url=None, docs_url=None)
db = Database(DB_NAME)['teacher']


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
        name, Teacher.new_token(), email, generate_password_hash(password)
    ).exec()
    return {
        'response': last_id
    }


@teacher.get('/id{teacher_id}')
async def get_teacher_by_id(teacher_id: int):
    """Получить преподавателя по ID

    :param teacher_id: ID преподавателя
    """
    result: Teacher = db.select().where(Val('teacher_id', teacher_id)).fetch_one_to(Teacher)
    del result.access_token
    del result.password
    return {
        'response': result.dict()
    }


@teacher.post('/auth')
async def login_teacher(email: str, password: str):
    """Вход через преподавателя

    :param email: E-mail преподавателя
    :param password: Пароль
    """
    result: Teacher = db.select().where(Val('email', email)).fetch_one_to(Teacher)
    if result is None:
        return HttpError.WRONG_EMAIL
    if not check_password_hash(result.password, password):
        return HttpError.WRONG_PASSWORD
    return {
        'response': {
            'access_token': result.access_token,
            'id': result.teacher_id
        }
    }
