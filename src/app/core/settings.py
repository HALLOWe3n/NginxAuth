import os

from dotenv import load_dotenv

ENV = load_dotenv("envs/.env")

# MARK:
# ----
# JWT
ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY_REFRESH = os.getenv('SECRET_KEY_REFRESH')
EXPIRED_TIME_ACCESS_TOKEN = int(os.getenv('EXPIRED_TIME_ACCESS_TOKEN'))
EXPIRED_TIME_REFRESH_TOKEN = int(os.getenv('EXPIRED_TIME_REFRESH_TOKEN'))
