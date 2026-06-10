import os
from flask import Flask

from .config import Config
from .extensions import db, login_manager
from .models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ساخت پوشه آپلود
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # login loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # register blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp
    from .music.routes import music_bp
    from .admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(music_bp)
    app.register_blueprint(admin_bp)

    # create tables
    with app.app_context():
        db.create_all()

    return app