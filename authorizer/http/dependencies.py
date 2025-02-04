import uuid
from typing import Annotated

from fastapi import Depends, Request

from authorizer.auth.exceptions import AuthTokenInvalidException
from authorizer.authorizer import Authorizer
from authorizer.http.exceptions import HTTPUnauthorizedException, HTTPTokenInvalidException, HTTPUserIsNotAdminException
from ..config import authorizer_config


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get(authorizer_config.cookie.name)
    if token is not None:
        return token
    raise HTTPUnauthorizedException


def get_user_id_from_token(token: Annotated[str, Depends(get_token_from_cookie)]) -> uuid.UUID:
    try:
        return Authorizer.get_user_id_from_token(token)
    except AuthTokenInvalidException:
        raise HTTPTokenInvalidException


def get_user_role_from_token(token: Annotated[str, Depends(get_token_from_cookie)]) -> str:
    try:
        return Authorizer.get_user_role_from_token(token)
    except AuthTokenInvalidException:
        raise HTTPTokenInvalidException


def check_user_is_admin(user_role: Annotated[str, Depends(get_user_role_from_token)]) -> None:
    if user_role != "Администратор":
        raise HTTPUserIsNotAdminException
