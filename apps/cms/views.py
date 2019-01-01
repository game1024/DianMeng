#encoding: utf-8
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g
)
from .forms import (
    LoginForm,
    ResetPwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm,
)

from .models import CMSUser, CMSPersmission
from apps.models import BannerModel, BoardModel, PostModel, HighlightPostModel
from ..front.models import FrontUser
from .decorators import login_required, permission_required
import config
from exts import db
from utils import restful, dmcache
import random, string
from tasks import send_mail
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func

bp = Blueprint("cms", __name__, url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # 31 Days
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message = 'Wrong email or password.')
        else:
            return self.get(message = 'Check your input format.')

@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # {"code":200, message="密码错误"}
                return restful.success()
            else:
                return restful.params_error("旧密码错误!")
        else:
             return restful.params_error(form.get_error())

@bp.route('/email_captcha/')
def email_captcha():
    #/email_capthca/?email=xxx@qq.com
    email = request.args.get('email')

    if not email:
        return restful.params_error('请传递邮箱参数!')

    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x), range(0, 10)))
    # source.extend(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    captcha = "".join(random.sample(source, 6))
    #使用Celery异步发送
    send_mail.delay('Reset your cms email of DianMeng.', [email], 'Your captcha is:%s'%captcha)
    dmcache.set(email, captcha)
    return restful.success()

class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())

bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))

@bp.route('/posts/')
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    post_list = PostModel.query.order_by(PostModel.create_time.desc())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    total = post_list.count()
    posts = post_list.slice(start, end)

    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)

    context = {
        'pagination' : pagination,
        'posts' : posts,
    }

    return render_template('cms/cms_posts.html', **context)

@bp.route('/hpost/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    post = PostModel.query.get(post_id)
    if post:
        highlight = HighlightPostModel()
        highlight.post = post
        db.session.add(highlight)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error('没有这篇帖子！')

@bp.route('/uhpost/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    if highlight:
        db.session.delete(highlight)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error('这篇帖子没有加精！')

@bp.route('/comments/')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')

@bp.route('/boards/')
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards' : board_models
    }
    return render_template('cms/cms_boards.html',  **context)

@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)

    if form.validate():
        name = form.name.data
        board = BoardModel(name = name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)

        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块!')

    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def dboard():
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error(message='请传入板块ID!')

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块!')

    db.session.delete(board)
    db.session.commit()
    return restful.success()

@bp.route('/fusers/')
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    fusers_list = FrontUser.query.outerjoin(PostModel).add_columns(FrontUser.id, FrontUser.email, FrontUser.username, FrontUser.join_time).\
        add_columns(func.count(PostModel.author_id).label("post_count")).group_by(FrontUser.id)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    total = fusers_list.count()

    fusers = fusers_list.slice(start, end)

    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)

    context = {
        'pagination' : pagination,
        'fusers' : fusers,
        'total': total,
    }
    return render_template('cms/cms_fusers.html', **context)

@bp.route('/dfusers/', methods=['POST'])
@login_required
def dfusers():
    fuser_id = request.form.get('fuser_id')
    if not fuser_id:
        return restful.params_error(message='参数错误!')

    fuser = FrontUser.query.get(fuser_id)

    if not fuser:
        return restful.params_error(message='没有此用户！')

    db.session.delete(fuser)
    db.session.commit()
    return restful.success()


@bp.route('/cusers/')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/croles/')
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')

@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()

    return render_template('cms/cms_banners.html', banners = banners)

@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id!')

    banner = BannerModel.query.get(banner_id)

    if not banner:
        return restful.params_error(message='没有这个轮播图')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/dpost/', methods=['POST'])
@login_required
def dpost():
    post_id = request.form.get('post_id')
    post = PostModel.query.get(post_id)

    if not post:
        return restful.params_error(message='数据库中无此帖')

    db.session.delete(post)
    db.session.commit()
    return restful.success()