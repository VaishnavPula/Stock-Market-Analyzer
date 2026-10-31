import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE = Path(__file__).resolve().parent
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'local-development-only-change-this')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE / 'instance' / 'stockvision.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
