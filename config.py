import os


class Config:
    # DATABASE = 'bwlgavuqyiep9jy89old'
    # DATABASE_USER = 'u5qgpo7x2p5ijga7onbe'
    # DATABASE_PASSWORD = '3T1d3uCIdyuLZ1VfU5B2'
    # DATABASE_HOST = 'bwlgavuqyiep9jy89old-postgresql.services.clever-cloud.com'
    DATABASE = 'mydb'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = 'peri54ri7end'
    DATABASE_HOST = 'localhost'

    SECRET_KEY = os.urandom(12)
