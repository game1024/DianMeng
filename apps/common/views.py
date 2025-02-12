#encoding: utf-8
from flask import Blueprint, request, make_response, jsonify
from twilio.rest import Client
from utils import restful, dmcache
import config
from .forms import SMSCaptchaForm
from utils.captcha import Captcha
from io import BytesIO
from tasks import send_mail
import random, string

bp = Blueprint("common", __name__, url_prefix='/c')

@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        email = form.email.data
        captcha = Captcha.gene_num(number=4)

        #twilio client
        # client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
        #
        # message = client.messages \
        #     .create(
        #     body="Your DianMeng's verification code is:%s." %captcha,
        #     from_='+14704129144',
        #     to='+86' + telephone,
        # )

        send_mail.delay('来自萌星的验证码', [email], '你的注册验证码为:%s' % captcha)

        print('发送邮件验证码为:',captcha)
        dmcache.set(email, captcha)
        return restful.success()
    else:
        return restful.params_error(message='请检查邮件格式')

@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    dmcache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    print('生成图片验证码为:',text)
    return resp

@bp.route('/uptoken/')
def uptoken():
    pass
    # access_key = 'PeJQbTqGQiCaXNyso7QOZQ9nufFKN8Is2MZhdcS9'
    # secret_key = 'SrkrQGgpME0U9yH3gLumaSOVgawKge80A8K7WyQg'
    # q = qiniu.Auth(access_key,secret_key)
    #
    # bucket = 'bbspic'
    # token = q.upload_token(bucket)
    # return jsonify({'uptoken':token})
