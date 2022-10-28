# -*- cdogin: utf-8 -*-
from .. import DatabaseType


class Mark(DatabaseType):
    template = ['m_id', 'score', 'title', 'subject_id', 'date']

    m_id: int
    score: int
    title: str
    subject_id: int
    date: int
