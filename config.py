import os
from dotenv import load_dotenv

load_dotenv()   # Load variables from .env file

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_URI = os.environ.get('MONGO_URI')