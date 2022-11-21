# -*- coding: utf-8 -*-
from fastapi import FastAPI

from config import ADMIN_TOKEN, DB_NAME
from database import Database
from database.types.teacher import Teacher
from models import AdminPayload

teacher = FastAPI(redoc_url=None, docs_url=None)

db = Database(DB_NAME)


@teacher.post('/')
async def create_teacher(
        name: str,
        email: str,
        password: str,
        payload: AdminPayload
):
    """Creates a new teacher

    :param name: teacher name
    :param email: E-mail
    :param password: account password
    :param payload: payload
    """
    if payload.admin_token != ADMIN_TOKEN:
        return {'error': 'You can not do it'}
    last_id = db.insert_one('teacher', 'name', 'access_token', 'email', 'password').values(
        name, Teacher.new_token(), email, password
    ).exec()
    return {
        'response': last_id
    }
