import typing as t
from werkzeug.exceptions import HTTPException
from flask import Response

import json


class APIException(HTTPException):
    code = 200
    error_code = 3000
    message = '服务器内部错误'
    data = None

    def __init__(self, error_code: int | None = None, message: int | None = None, data=None) -> None:
        if error_code is not None:
            self.error_code = error_code
        if message is not None:
            self.message = message
        if data is not None:
            self.data = data
        super().__init__(message, None)

    def get_body(self, environ=None, scope: dict | None = None) -> bytes:
        body = dict(
            code=self.error_code,
            message=self.message,
            data=self.data
        )
        return json.dumps(body)

    def get_headers(
        self,
        environ=None,
        scope: dict | None = None,
    ) -> list[tuple[str, str]]:
        """Get a list of headers."""
        return [('Content-Type', 'application/json;charset=utf-8')]

    def to_dict(self):
        return dict(
            code=self.error_code,
            message=self.message,
            data=self.data
        )

    @classmethod
    def ok(cls, data=None):
        return cls(1000, '', data)
