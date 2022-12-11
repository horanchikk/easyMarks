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
async def teacher_create(
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
    :return: Новый ID преподавателя:
    ```json
    {"response": 5}
    ```
    """
    if payload.admin_token != ADMIN_TOKEN:
        return HttpError.ADMIN_ACCESS_REQUIRE
    last_id = db.insert_one('teacher', 'name', 'access_token', 'email', 'password', 'admin').values(
        name, Teacher.new_token(), email, generate_password_hash(password), False
    ).exec()
    return {'response': last_id}


@teacher.get('/id{teacher_id}')
async def teacher_by_id(teacher_id: int):
    """Получить преподавателя по ID

    :param teacher_id: ID преподавателя
    :return: Объект преподавателя
    ```json
{
  "response": {
        "admin": "1",
    "teacher_id": 1,
    "name": "Морозов Вадим Валерьевич",
    "email": "horanchikk@gmail.com",
  }
}
    ```
    """
    result: Teacher = db.select().where(Val('teacher_id', teacher_id)).fetch_one_to(Teacher)
    if result is None:
        return HttpError.INVALID_TEACHER_ID
    del result.access_token
    del result.password
    return {'response': result.dict()}


@teacher.post('/auth')
async def teacher_login(email: str, password: str):
    """Вход через преподавателя

    :param email: E-mail преподавателя
    :param password: Пароль
    :return: Вход в аккаунт преподавателя
    ```json
{
  "response": {
    "access_token": "...",
    "id": 0
  }
}
    ```
    """
    result: Teacher = db.select().where(Val('email', email)).fetch_one_to(Teacher)
    if result is None:
        return HttpError.WRONG_EMAIL
    if not check_password_hash(result.password, password):
        return HttpError.WRONG_PASSWORD
    return {
        'response': {
            'access_token': result.access_token,
            'id': result.teacher_id,
            'admin': True if result.admin == "1" else False
        }
    }
