# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, Val
from database.types.student import Student
from config import DB_NAME


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
