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
        subjects_ids: str,
        payload: AdminPayload
):
    """Creates a new teacher

    :param name: teacher name
    :param subjects_ids: subjects IDs separated by ,
    :param payload: payload
    """
    if payload.admin_token != ADMIN_TOKEN:
        return {'error': 'You can not do it'}
    db.insert_one('teacher', 'name', 'subjects_ids', 'access_token').values(
        name, subjects_ids, Teacher.new_token()
    )
    return {
        'response': db.exec()
    }
