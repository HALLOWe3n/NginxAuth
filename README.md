## Authentication Server

### Start the process manually:

Python version:
  - Python 3.8.1

***
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