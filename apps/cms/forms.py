# -*- coding: utf-8 -*-
__author__ = 'jimmy'
#encoding: utf-8
from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from apps.forms import BaseForm
from wtforms import ValidationError
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='Invalid email format!'), InputRequired('Input an email!')])
    password = StringField(validators=[Length(6, 20, message='Between 6 and 20 characters!')])
    remember = IntegerField()

class ResetPwdForm(BaseForm):
    oldpwd  = StringField(validators=[Length(6, 20, message='输入正确格式旧密码')])
    newpwd  = StringField(validators=[Length(6, 20, message='输入正确格式新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message='确认新旧密码保持一致')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[ Email( message='请输入正确格式邮箱!' ) ])
    captcha = StringField(validators=[ Length(min=6, max=6, message='验证码长度为6')])

    def validate_email(self, field):
        email = field.data
        user = g.cms_user

        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱!')

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称!')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接!')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接!')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级!')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图ID!')])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称!')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id!')])