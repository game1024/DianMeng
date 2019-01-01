#encoding: utf-8
import os

SECRET_KEY = os.urandom(24)

DEBUG = True

#MySql
#create database if not exists dianmeng charset utf8 collate utf8_general_ci
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'dianmeng'
DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

#CMS User
CMS_USER_ID = 'twethuWT'
#Front User
FRONT_USER_ID = 'xbvDAert'

# MAIL qq
MAIL_SERVER = "smtp.126.com"
MAIL_PORT = '25'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "yellowcrayon@126.com"
MAIL_PASSWORD = "mail126"
MAIL_DEFAULT_SENDER = "yellowcrayon@126.com"
MAIL_DEBUG = True


#SMS twilio
ACCOUNT_SID = 'AC1cfb11fd6e3735e02616e92de9a731e0'
AUTH_TOKEN = '5cd528e7b6e7162d586a9b2ac2c3ae90'

#UEditor
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'images')
UEDITOR_UPLOAD_TO_QINIU = False
UEDITOR_QINIU_ACCESS_KEY = "PeJQbTqGQiCaXNyso7QOZQ9nufFKN8Is2MZhdcS9"
UEDITOR_QINIU_SECRET_KEY = "SrkrQGgpME0U9yH3gLumaSOVgawKge80A8K7WyQg"
UEDITOR_QINIU_BUCKET_NAME = "bbspic"
UEDITOR_QINIU_DOMAIN = "http://pis6hkx1k.bkt.clouddn.com/"

#Paginate
PER_PAGE = 10


#Celery相关
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_TASK_SERIALIZER = "json"
