import typing

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request, Form, HTTPException

from starlette.status import HTTP_303_SEE_OTHER
from starlette.responses import RedirectResponse

from ..models.auth import Auth
from ..models.structs import User, BearerStructure

router = APIRouter()
templates = Jinja2Templates(directory='/templates')


@router.post('/refresh')
def refresh_token(payload: BearerStructure):
    """
    \f
    :param payload:
    :return:
    """
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
        redirect_uri: str = Form('redirect_uri'),
):
    if redirect_uri == 'None':
        raise HTTPException(status_code=400, detail='None have redirect uri')
    auth = Auth()
    user_payload = auth.check_user(username=username, password=password)
    bearer_tokens = auth.create_tokens(payload=user_payload)

    authorization_headers = {'Authorization': f'Bearer {bearer_tokens["access_token"]}'}

    return RedirectResponse(
        redirect_uri,
        status_code=HTTP_303_SEE_OTHER,
        headers=authorization_headers
    )


@router.get('/example')
def example_redirect(user: User = Depends(Auth().get_user)):
    return {'message': 'success'}


@router.get('/auth')
def check_auth_user(user: User = Depends(Auth().get_user)) -> typing.Dict:
    return {'Authorization': True}
