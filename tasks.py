#encoding: utf-8
from celery import Celery
from flask_mail import Message
from exts import mail
from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)

#运行本文件win
#celery -A tasks.celery worker --pool=solo --loglevel=info
#运行本文件linux
#celery -A tasks.celery worker --loglevel=info

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task
def send_mail(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message)

@celery.task
def send_sms_captcha(telephone, captcha):
    pass
