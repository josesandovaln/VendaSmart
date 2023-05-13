from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '769c32c922ca8225ec53696091b437bf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdv.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Para acessar a página, realize login'
login_manager.login_message_category = 'alert-warning'

from site_atividade import routers

