from flask import Flask
from flask_login import LoginManager , UserMixin
from src.dash.dash import dash_app
from src.models.models import db, User
from dash import html

DB_NAME ='dash.db'
def create_app_flask():
    server = Flask(__name__)
    server.config['SECRET_KEY'] = '5f352379324c22463451387a0aec5d2f'
    server.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(server)
    
    with server.app_context():
        db.create_all()
    
    #server.register_blueprint(views.views, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = '/login'
    login_manager.init_app(server)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    
    return server


def run_dash():
    app = create_app_flask()
    dash_app.init_app(app)
    dash_app.run(debug = True)