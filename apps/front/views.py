#encoding: utf-8
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    abort
)

from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from utils import restful, safeutils
from .models import FrontUser
from apps.models import BannerModel, BoardModel, PostModel, CommentModel, HighlightPostModel
from exts import db
import config
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func

bp = Blueprint("front", __name__)

@bp.route('/')
def index():
    search_content = request.args.get("search_content")

    board_id = request.args.get('bd', type=int, default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get("sort", type=int, default=1)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    posts = None
    total = 0
    query_obj = None

    if sort == 1:
        # 发表时间
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 加精时间
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        # 阅读数量
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 评论数量
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())
    else:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())


    if search_content:
        query_obj = PostModel.query.filter(PostModel.title.contains(search_content))
    else:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())


    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        query_obj = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        query_obj = query_obj.slice(start, end)
        total = query_obj.count()

    pagination = Pagination(bs_version=3, page=3, total=2, outer_window=0, inner_window=2)

    context = {
        'banners' : banners,
        'boards' : boards,
        'posts' : query_obj,
        'pagination' : pagination,
        'current_board' : board_id,
        'current_sort' : sort,
        'search_content' : search_content,
    }
    return render_template('front/front_index.html', **context)


@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)

    if not post:
        abort(404)
    else:
        post.read_num += 1
        db.session.commit()

    comments = CommentModel.query.filter_by(post_id=post_id).all()
    return render_template('front/front_pdetail.html', post=post, comments=comments)

@bp.route('/acomment/', methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            post.comment_num += 1
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子!')
    else:
        return restful.params_error(form.get_error())


@bp.route('/apost/', methods=['GET','POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards = boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块!')
            post = PostModel(title = title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

@bp.route('/test/')
def front_test():
    return render_template('front/front_test.html')

class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer

        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to = return_to)
        else:
            return render_template('front/front_signup.html')

        # return render_template('front/front_signin.html')

    def post (self):
        form = SignupForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(email=email, username = username, password = password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to = return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)

        if form.validate():
            email = form.email.data
            password  = form.password.data
            remember = form.remeber.data


            user = FrontUser.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='邮箱或者密码错误!')

        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))


@bp.route('/logout/')
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return_to = request.referrer
    return render_template('front/front_signin.html', return_to=return_to)
