import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///evs.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False