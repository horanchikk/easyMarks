# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, Val
from database.types.mark import Mark
from config import DB_NAME


mark = FastAPI(redoc_url=None, docs_url=None)
db = Database(DB_NAME)


@mark.get('/id{m_id}')
async def get_mark_by_id(m_id: int):
    """Finds mark by its ID"""
    result = db.select('mark').where(Val('m_id', m_id)).fetch_one_to(Mark)
    return {
        'response': result.dict()
    }
