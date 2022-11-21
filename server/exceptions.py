# -*- coding: utf-8 -*-
from enum import Enum

from fastapi.responses import JSONResponse
from fastapi import status


def exception_response(code: int, msg: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'error': {'message': msg, 'code': code}}
    )


class HttpError:
    ADMIN_ACCESS_REQUIRE = exception_response(0, "You hasn't access")
    WRONG_ACCESS_TOKEN = exception_response(1, "Wrong access token")
