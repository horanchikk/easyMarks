# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, Column
from database.types.subject import Subject
from config import DB_NAME


subject = FastAPI(redoc_url=None, docs_url=None)

db = Database(DB_NAME)


@subject.post('/')
async def create_subject(
        title: str,
        teacher_id: int,
        groups: str
):
    """Creates a new subject

    :param title: subject name
    :param teacher_id: Teacher ID
    :param groups: Group IDs separated by ,
    """
    last_id = db.insert_one(
        'subject', 'title', 'teacher_id', 'groups'
    ).values(title, teacher_id, groups).exec()
    return {
        'response': last_id
    }
