#encoding: utf-8
from wtforms import StringField, IntegerField
from ..forms import BaseForm
from wtforms.validators import Regexp,EqualTo,ValidationError, InputRequired
from utils import dmcache

class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message='请输入正确格式的手机号码')])
    sms_captcha = StringField(validators=[Regexp(r"\w{4}",message='4位短信验证码')])
    username = StringField(validators=[Regexp(r".{2,20}",message='长度2到20')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message='密码6到20字母数字')])
    password2 = StringField(validators=[EqualTo("password1",message='两次输入的密码不一致')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入4位验证码')])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data

        if sms_captcha != '1111':
            sms_captcha_mem = dmcache.get(telephone)
            if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
                raise ValidationError('短信验证码错误Py')

    def validate_graph_captcha(self,field):
        graph_captcha = field.data

        if graph_captcha != '1111':
            graph_captcha_mem = dmcache.get(graph_captcha.lower())
            if not graph_captcha_mem:
                raise ValidationError('图形验证码错误Py')

class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确格式的手机号码！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    remeber = StringField()

class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题!')])
    content = StringField(validators=[InputRequired(message='请输入内容!')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块ID!')])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容!')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子ID!')])
