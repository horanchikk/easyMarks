# -*- coding: utf-8 -*-
from enum import Enum

from fastapi.responses import JSONResponse
from fastapi import status


def err_response(code: int, msg: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'error': {'message': msg, 'code': code}}
    )


class HttpError:
    ADMIN_ACCESS_REQUIRE = err_response(0, "You hasn't access")
    WRONG_ACCESS_TOKEN = err_response(1, "Wrong access token")
    INVALID_SUBJECT_ID = err_response(2, "Invalid subject ID")
    INVALID_STUDENT_ID = err_response(3, "Invalid student ID")
    HAS_NT_SUBJECT = err_response(4, "This student hasn't this subject")
    NOT_ACCESS_TO_THIS_SUBJECT = err_response(5, "Haven't access to this subject")
    THIS_STUDENT_HAS_NT_SBJ = err_response(6, "This student hasn't this subject")
    WRONG_PASSWORD = err_response(7, "Wrong password")
    WRONG_EMAIL = err_response(8, "Wrong email")
    INVALID_GROUP_ID = err_response(9, "Invalid group ID")
    INVALID_TEACHER_ID = err_response(10, "Invalid teacher ID")
