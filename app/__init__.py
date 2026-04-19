from flask import Flask
from app.extensions import db,login_manager
from config import Config
from werkzeug.security import generate_password_hash
from app.blueprints.auth import auth_bp
from app.blueprints.admin import admin_bp
from app.blueprints.company import company_bp
from app.blueprints.student import student_bp
from app.models import User
def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(company_bp,url_prefix='/company')
    app.register_blueprint(student_bp,url_prefix='/student')
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role='admin').first():
            admin=User(name='admin',
                   email='admin@gmail.com',
                   password=generate_password_hash('1234sriram'),
                   role='admin')
            db.session.add(admin)
            db.session.commit()
    return app