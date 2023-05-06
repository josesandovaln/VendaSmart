from datetime import datetime
from site_atividade import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    usuario = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

class Produtos(database.Model):
    id_produtos = database.Column(database.Integer, primary_key=True)
    produto = database.Column(database.String, nullable=False)
    preco = database.Column(database.Float, nullable=False)
    estoque = database.Column(database.Integer, nullable=False)
    categoria_fk = database.Column(database.Integer, database.ForeignKey('categoria.id_categoria'), nullable=False)
    venda = database.relationship('Venda', backref='produto')


class Categoria(database.Model):
    id_categoria = database.Column(database.Integer, primary_key=True)
    categoria = database.Column(database.String, nullable=False)
    produtos = database.relationship('Produtos', backref='categoria', lazy=True)

class Venda(database.Model):
    id_venda = database.Column(database.Integer, primary_key=True)
    produto_id = database.Column(database.Integer, database.ForeignKey('produtos.id_produtos'), nullable=False)
    quantidade = database.Column(database.Integer, nullable=False)
    total = database.Column(database.Float, nullable=False)

class Pagamento(database.Model):
    id_pagamento = database.Column(database.Integer, primary_key=True)
    metodo_pagamento = database.Column(database.String, nullable=False)
    valor_pagamento = database.Column(database.Float, nullable=False)
    troco = database.Column(database.Float)
    data_pagamento = database.Column(database.DateTime, default=datetime.now, nullable=False)




