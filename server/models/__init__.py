# -*- coding: utf-8 -*-
from pydantic import BaseModel


class AdminPayloadModel(BaseModel):
    admin_token: str
