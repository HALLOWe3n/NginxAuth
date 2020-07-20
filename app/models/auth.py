import jwt
import typing
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from ..core import settings
from ..models.structs import User
from ..models.database import user_fake_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class Auth:
    def __init__(self):
        self.__algorithm = settings.ALGORITHM
        self.__secret_key = settings.SECRET_KEY
        self.__secret_key_refresh = settings.SECRET_KEY_REFRESH

        # Default expired times for access and refresh tokens
        self.__expired_time = timedelta(minutes=settings.EXPIRED_TIME_ACCESS_TOKEN)
        self.__expired_time_refresh = timedelta(days=settings.EXPIRED_TIME_REFRESH_TOKEN)

    def fake_hash_password(self, password: str):
        return f'fakehashed{password}'

    def check_user(self, username: str, password: str):
        user = user_fake_db.get(username, None)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        if user['password'] == self.fake_hash_password(password=password):
            return user
        else:
            raise HTTPException(status_code=401, detail="Incorrect username or password")

    def get_user(self, token: str = Depends(oauth2_scheme)) -> User:
        """
        Get user from database and pack in dict.

        :return: payload {'username': username, 'password': password}
        """
        user = self.validate_token(token)
        return user

    def create_tokens(self, payload: typing.Dict) -> typing.Dict:
        """
        Create and return auth JWT tokens

        :param payload: dict user info for
        :return: Bearer tokens dict(access_token, refresh_token)
        """

        payload.update({'exp': datetime.utcnow() + self.__expired_time})
        access_token = jwt.encode(payload, self.__secret_key, algorithm=self.__algorithm).decode('utf-8')

        payload.update({'exp': datetime.utcnow() + self.__expired_time_refresh})
        refresh_token = jwt.encode(payload, self.__secret_key, algorithm=self.__algorithm).decode('utf-8')

        bearer_tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        return bearer_tokens

    def validate_token(self, token: str, is_refresh: bool = False) -> typing.Dict or User:
        """
        Validate user token and return dict user.

        :param token: tokens [access/refresh]
        :param is_refresh: True if token is `refresh_token` or False if `access_token`
        :return: payload with user info if token is access or former a new bearer_info if token is refresh
        """
        try:
            payload = jwt.decode(
                token,
                self.__secret_key_refresh if is_refresh else self.__secret_key,
                algorithms=self.__algorithm
            )
            user_data = self.__create_user_struct(payload=payload)
        except jwt.ExpiredSignature:
            raise HTTPException(status_code=401, detail='Token Expired!')
        except (jwt.DecodeError, jwt.InvalidSignatureError):
            raise HTTPException(status_code=401, detail='Invalid token!')

        return self.create_tokens(payload) if is_refresh else user_data

    def __create_user_struct(self, payload: typing.Dict):
        """
        Get decode payload from self.validate_token().
        Create dict for searching in table, and
        Create User Pydantic structure

        :param payload: (oauth2 access token) decode payload
        :return: User: pydantic model
        """
        username = payload['username']
        _user_in_db = user_fake_db.get(username, None)
        if _user_in_db:
            return User(username=_user_in_db['username'], password=_user_in_db['password'])
        raise HTTPException(status_code=401, detail="Incorrect username or password")