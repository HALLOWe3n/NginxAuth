import typing
from pprint import pprint

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, Request, Form, HTTPException

from starlette.status import HTTP_303_SEE_OTHER

from ..models.auth import Auth
from ..models.structs import User, BearerStructure

router = APIRouter()
templates = Jinja2Templates(directory='src/templates')


@router.post('/refresh/token')
def refresh_token(payload: BearerStructure):
    """
    \f
    :param payload:
    :return:
    """
    print(payload.refresh_token)
    bearer_info = Auth().validate_token(token=payload.refresh_token, is_refresh=True)
    return bearer_info


@router.get('/login', status_code=200)
def login_template(request: Request):
    """
    \f
    :return: dict
    """
    return templates.TemplateResponse('index.html', context={'request': request})


@router.post('/just/login', name='login_user')
def login_user(
        username: str = Form('username'),
        password: str = Form('password'),
):
    auth = Auth()
    user_payload = auth.check_user(username=username, password=password)
    bearer_tokens = auth.create_tokens(payload=user_payload)

    return bearer_tokens


@router.get('/example')
def example_redirect():
    return {'message': 'success'}


@router.get('/new/example')
def new_example_redirect(user: User = Depends(Auth().get_user)):
    return {'message': 'success'}


@router.get('/auth', name='auth')
def check_auth_user(user: User = Depends(Auth().get_user)) -> typing.Dict:
    return {'Authorization': True}
