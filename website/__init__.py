from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db=SQLAlchemy()

DB_NAME="mydatabase.db"

def create_app():

    app = Flask(__name__)

    app.secret_key = "Super Secret Key"
    # database configuration goes here!
    app.config ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)#Initialzing the database here!

# importng and registrering the blurprint here!
    from .views import views
    from .auth import auths

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auths,url_prefix='/auths/')
# creating the tble of the database here!

    from .models import User,Note
    with app.app_context():
        db.create_all() #creating the database here!

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auths.login'

    @login_manager.user_loader
    def load_user(id):
        try:
            return User.query.filter(User.id == id).first()
        
        except models.DoesNotExist :
            return None
   
    return app
