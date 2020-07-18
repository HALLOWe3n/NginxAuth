import uvicorn

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.app.routes.users import router as users_router

app = FastAPI(title='Authentication Service', version='0.1')
app.mount("/static", StaticFiles(directory='src/static'), name='static')

app.include_router(users_router)


if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=5000)
