from typing import Tuple

from flask import jsonify, Response
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str


def success_response(message: str="ok") -> Tuple[Response, int]:
    return jsonify(SuccessResponse(status=message).model_dump()), 200


def error_response(message: str, status: int=200) -> Tuple[Response, int]:
    return jsonify(ErrorResponse(message=message).model_dump()), status
