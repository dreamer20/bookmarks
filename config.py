import os


class Config:
    DATABASE = 'mydb'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = 'peri54ri7end'
    DATABASE_HOST = 'localhost'
    SECRET_KEY = os.urandom(12)
