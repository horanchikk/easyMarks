# -*- coding: utf-8 -*-
from pydantic import BaseModel


class AdminPayload(BaseModel):
    admin_token: str
