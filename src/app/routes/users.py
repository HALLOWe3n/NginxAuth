import json
import typing

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request, Form

from starlette.responses import RedirectResponse

from src.app.models.auth import Auth
from src.app.models.structs import User, BearerStructure

router = APIRouter()
templates = Jinja2Templates(directory='src/templates')


@router.post('/refresh')
def refresh_token(payload: BearerStructure):
    """
    \f
    :param payload:
    :return:
    """
    # TODO: fix refresh token decode
    bearer_info = Auth().validate_token(token=payload.refresh_token, is_refresh=True)
    return bearer_info


@router.get('/login', status_code=200)
def login_template(request: Request):
    """
    \f
    :return: dict
    """
    return templates.TemplateResponse('index.html', context={'request': request})


@router.post('/login/user', name='login_user')
def login_user(username: str = Form('username'), password: str = Form('password')):
    auth = Auth()
    user_payload = auth.check_user(username=username, password=password)

    bearer_tokens = auth.create_tokens(payload=user_payload)

    # TODO: get redirect URI from `request` object
    redirect_uri = 'http://localhost:5000/example_redirect'
    # TODO: pack payload and fix bytes tokens
    payload = {**bearer_tokens, 'status': 200}

    return RedirectResponse(url=redirect_uri, headers=bearer_tokens)


@router.get('/example_redirect')
def example_redirect(request: Request):
    return {'message': 'success'}


@router.get('/auth', status_code=200)
def check_auth_user(user: User = Depends(Auth().get_user)) -> typing.Dict:
    """
    \f
    :param user:
    :param status_code:
    :return:
    """
    return {'user': user.username}
