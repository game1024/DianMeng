from flask import Flask

from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp

import config
from exts import db, mail
from flask_wtf import CSRFProtect
from utils.captcha import Captcha

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    db.init_app(app)
    CSRFProtect(app)
    return app

Captcha.gene_graph_captcha()

app = create_app()

if __name__ == '__main__':
    app.run('')
