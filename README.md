## Authentication Server

### Definition to run in Docker:

```bash
docker-compose up --build -d
```

### Start the process manually:

Python version:
  - Python 3.8.1

***
### Important
Make sure you have nginx running

then replace the default nginx config ```default.conf```
to the content of the module ```not_docker_nginx.conf``` 

install dependencies from ```requirements.txt``` file

```bash
pip install -r requirements.txt
```
then go to the directory ```app/``` and execute the module ```main.py```
or in the root directory run the command:

```bash
uvicorn app.main:api --host=0.0.0.0 --port=8000 --reload
```

Enjoy!