from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

"""
Flask App Object (`app`):
  - app: Objeto Flask responsável por criar e configurar a aplicação Flask.

Configuration:
  - SECRET_KEY: Chave secreta utilizada para proteger as sessões e cookies na aplicação.
  - SQLALCHEMY_DATABASE_URI: URL de conexão com o banco de dados SQLite.

Database:
  - database: Objeto SQLAlchemy que representa o banco de dados e permite a interação com ele.

Password Hashing:
  - bcrypt: Objeto Bcrypt responsável por realizar o hashing de senhas.

Login Manager:
  - login_manager: Objeto LoginManager responsável por gerenciar a autenticação de usuários.
    - login_view: Rota para redirecionar os usuários não autenticados para a página de login.
    - login_message: Mensagem exibida aos usuários não autenticados ao acessar uma página protegida.
    - login_message_category: Categoria da mensagem exibida aos usuários não autenticados.
"""

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

