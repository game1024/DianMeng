#encoding: utf-8
from .views import bp
import config
from flask import session, g
from .models import CMSUser, CMSPersmission

@bp.before_request
def cms_before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user;


@bp.context_processor
def cms_context_processor():
    return {"CMSPermission":CMSPersmission}