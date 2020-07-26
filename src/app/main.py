from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from .routes.users import router as users_router


api = FastAPI(title='Authentication Service', version='0.1')
api.mount("/static", StaticFiles(directory='src/static'), name='static')
api.include_router(users_router)
