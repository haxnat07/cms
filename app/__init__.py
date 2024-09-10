from flask import Flask,request
from app.extensions import *
from config import Config
from app.extensions import db
from app.auth.models import *

from werkzeug.utils import secure_filename
from flask import redirect, url_for
import os



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    

    from app.main import main_bp
    from app.auth import auth_bp
    

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.auth.models import User  # Import inside function to avoid circular import
    return User.query.get(int(user_id))