# -*- coding: utf-8 -*-
from fastapi import FastAPI

from config import DB_NAME, ADMIN_TOKEN
from database import Database
from database.types.group import Group
from exceptions import HttpError
from models import AdminPayloadModel

group = FastAPI(docs_url=None, redoc_url=None)
db = Database(DB_NAME)


@group.post('/')
async def create_new_group(
        name: str,
        payload: AdminPayloadModel
):
    """Создает новую группу

    :param name: название группы
    :param payload: полезная нагрузка
    """
    if payload.admin_token != ADMIN_TOKEN:
        return HttpError.ADMIN_ACCESS_REQUIRE
    result = db.insert_one('studentGroup', 'name').values(name).exec()
    return {
        'response': result
    }


@group.get('/all')
async def get_all_groups():
    """Возвращает все группы
    """
    result = db.select('group').fetch_to(Group)
    return {
        'response': {
            'items': [i.dict() for i in result],
            'size': len(result)
        }
    }
