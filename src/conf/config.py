# from dotenv import load_dotenv
# load_dotenv()

from pydantic import BaseSettings

import os
# sqlalchemy_database_url = os.environ.get('API_KEY')
# secret_key = os.environ.get('SECRET_KEY')
# debug = os.environ.get('DEBUG')
# start_page_off = os.environ.get('START_PAGE_OFF')

class Settings(BaseSettings):
    sqlalchemy_database_url: str = 'postgresql+psycopg2://user:password@localhost:5432/postgres'
    secret_key: str = 'secret_key'
    algorithm: str = 'HS256'
    mail_username: str = 'example@meta.ua'
    mail_password: str = 'password'
    mail_from: str = 'example@meta.ua'
    mail_port: int = 465
    mail_server: str = 'smtp.meta.ua'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str = 'password'
    cloudinary_name: str = 'name'
    cloudinary_api_key: str = 326488457974591
    cloudinary_api_secret: str = 'secret'
    start_page_off: str = 'https://jobs.dou.ua/login/?next=/'
    selenium_username: str = 'user[email]'
    selenium_password: str = 'user[password]'
    main_page: str = 'https://jobs.dou.ua'
    off_code: str = 'GR'
    gr_code: str = 'GR'
    satis_url: str = 'https://jobs.dou.ua/companies/satisfactions/'
    gider_url: str = 'https://jobs.dou.ua/companies/gideros-mobile/'
    kasas_url: str = 'kasa/'
    off_tl_kasa_url: str = "123"
    gr_tl_kasa_url: str = "123"
    gr_usd_kasa_url: str = "123"
    gr_eur_kasa_url: str = "123"
    gr_transit_kasa_url: str = "123"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
