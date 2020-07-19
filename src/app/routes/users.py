import typing

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse

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
def login_user(request: Request, username: str = Form('username'), password: str = Form('password')):
    auth = Auth()
    user_payload = auth.check_user(username=username, password=password)
    bearer_tokens = auth.create_tokens(payload=user_payload)
    redirect_uri = request.headers['referer'].split('?url=')[1]

    return RedirectResponse(redirect_uri, status_code=302,
                            headers={'Authorization': f'Bearer {bearer_tokens["access_token"]}'})


@router.get('/example')
def example_redirect(user: User = Depends(Auth().get_user)):
    return {'message': 'success'}


@router.get('/auth')
def check_auth_user(user: User = Depends(Auth().get_user)) -> typing.Dict:
    return {'Authorization': True}
