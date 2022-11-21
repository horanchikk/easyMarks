# -*- coding: utf-8 -*-
from fastapi import FastAPI

from config import DB_NAME, ADMIN_TOKEN
from database import Database
from database.types.group import Group
from models import AdminPayload

group = FastAPI(docs_url=None, redoc_url=None)
db = Database(DB_NAME)


@group.post('/')
async def create_new_group(
        name: str,
        payload: AdminPayload
):
    """Creates a new group

    :param name: group name
    :param payload: Admin payload with token
    """
    if payload.admin_token != ADMIN_TOKEN:
        return {'error': 'You can not do it'}
    result = db.insert_one('studentGroup', 'name').values(name).exec()
    return {
        'response': result
    }


@group.get('/all')
async def get_all_groups():
    """Returns all groups"""
    result = db.select('group').fetch_to(Group)
    return {
        'response': {
            'items': [i.dict() for i in result],
            'size': len(result)
        }
    }
