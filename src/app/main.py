import uvicorn

from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from src.app.routes.users import router as users_router


api = FastAPI(title='Authentication Service', version='0.1')
api.mount("/static", StaticFiles(directory='src/static'), name='static')
api.include_router(users_router)


# @api.middleware('http')
# def set_headers_from_cookie(request: Request, call_next):
#     """
#
#     :param request:
#     :return:
#     """
#     print(request.headers["Authorization"])
#     response = call_next(request)
#     return response

if __name__ == '__main__':
    uvicorn.run(api, host='127.0.0.1', port=8000)
