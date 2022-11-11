# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, Column, Val
from database.types.subject import Subject
from config import DB_NAME, ADMIN_TOKEN
from models import AdminPayload

subject = FastAPI(redoc_url=None, docs_url=None)

db = Database(DB_NAME)


@subject.get('/id{subject_id}')
async def get_subject(subject_id: int):
    """Finds subject by ID

    :param subject_id: subject ID
    """
    subject = db.select('subject').where(Val('s_id', subject_id)).fetch_one_to(Subject)
    return {
        'response': subject.dict()
    }


@subject.post('/')
async def create_subject(
        title: str,
        teacher_id: int,
        groups: str,
        payload: AdminPayload
):
    """Creates a new subject

    :param title: subject name
    :param teacher_id: Teacher ID
    :param groups: Group IDs separated by ,
    :param payload: payload
    """
    if payload.admin_token != ADMIN_TOKEN:
        return {'error': 'You can not do it'}
    last_id = db.insert_one(
        'subject', 'title', 'teacher_id', 'groups'
    ).values(title, teacher_id, groups).exec()
    return {
        'response': last_id
    }
