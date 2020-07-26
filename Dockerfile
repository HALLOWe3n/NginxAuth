FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/app /app/app
COPY src/static /static
COPY src/templates /templates