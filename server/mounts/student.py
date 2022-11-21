# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, Val
from database.types.student import Student
from config import DB_NAME, ADMIN_TOKEN
from models import AdminPayload

student = FastAPI(docs_url=None, redoc_url=None)
db = Database(DB_NAME)


@student.get('/id{student_id}')
async def get_student_by_id(student_id: int):
    """Finds user by its ID

    :param student_id: Student ID
    """
    result = db.select('student').where(Val('s_id', student_id)).fetch_one_to(Student)
    return {
        'response': result.dict()
    }


@student.get('/group{group_id}')
async def get_student_by_group(group_id: int):
    """Finds users by group ID

    :param group_id: Group ID
    """
    result = db.select('student').where(Val('group_id', group_id)).fetch_to(Student)
    return {
        'response': {
            'items': [i.dict() for i in result],
            'size': len(result)
        }
    }


@student.post('/')
async def create_teacher(
        name: str,
        group_id: int,
        payload: AdminPayload
):
    """Creates a new teacher

    :param name: teacher name
    :param group_id: group ID
    :param payload: payload
    """
    if payload.admin_token != ADMIN_TOKEN:
        return {'error': 'You can not do it'}
    last_id = db.insert_one('student', 'name', 'group_id').values(
        name, group_id
    ).exec()
    return {
        'response': last_id
    }
