from datetime import datetime
from site_atividade import database, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):

    """
    Função de carregamento de usuário para o LoginManager.

    Parâmetros:
        id_usuario (str): O ID do usuário a ser carregado.

    Retorna:
        Usuario: O objeto Usuario correspondente ao ID do usuário.

    """

    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):

    """
    Classe do modelo de usuário.

    Atributos:
        id (database.Column): Coluna de chave primária para o ID do usuário.
        usuario (database.Column): Coluna para o nome de usuário.
        email (database.Column): Coluna para o endereço de e-mail do usuário.
        senha (database.Column): Coluna para a senha do usuário.

    Métodos:
        verificar_senha(senha): Verifica se a senha fornecida corresponde à senha armazenada no objeto Usuario.
        set_senha(nova_senha): Define a senha do usuário com base na nova senha fornecida.

    """

    id = database.Column(database.Integer, primary_key=True)
    usuario = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

    def verificar_senha(self, senha):

        """
        Verifica se a senha fornecida corresponde à senha armazenada no objeto Usuario.

        Parâmetros:
            senha (str): A senha a ser verificada.

        Retorna:
            bool: True se a senha corresponder, False caso contrário.
        """

        if bcrypt.check_password_hash(self.senha, senha):
            return True
        return False

    def set_senha(self, nova_senha):

        """
        Define a senha do usuário com base na nova senha fornecida.

        Parâmetros:
            nova_senha (str): A nova senha a ser definida.
        """

        self.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')

class Produtos(database.Model):

    """
    Classe do modelo de Produtos.

    Atributos:
        id_produtos (database.Column): Coluna de chave primária para o ID do produto.
        produto (database.Column): Coluna para o nome do produto.
        marca (database.Column): Coluna para a marca do produto.
        preco_aquisicao (database.Column): Coluna para o preço de aquisição do produto.
        preco (database.Column): Coluna para o preço de venda do produto.
        estoque (database.Column): Coluna para a quantidade em estoque do produto.
        margem_lucro (database.Column): Coluna para a margem de lucro do produto.
        categoria_fk (database.Column): Coluna para a chave estrangeira da categoria do produto.
        itens_venda (database.relationship): Relacionamento com a classe ItemVenda.

    Métodos:
        calcular_margem_lucro(): Calcula a margem de lucro do produto com base no preço de aquisição e de venda.
        __init__(produto, marca, preco_aquisicao, preco, estoque, categoria_fk): Construtor da classe Produtos.
        __repr__(): Retorna uma representação textual do objeto Produtos.

    """

    id_produtos = database.Column(database.Integer, primary_key=True)
    produto = database.Column(database.String, nullable=False)
    marca = database.Column(database.String, nullable=False)
    preco_aquisicao = database.Column(database.Float, nullable=False)
    preco = database.Column(database.Float, nullable=False)
    estoque = database.Column(database.Integer, nullable=False)
    margem_lucro = database.Column(database.Float, nullable=True)
    categoria_fk = database.Column(database.Integer, database.ForeignKey('categoria.id_categoria'), nullable=False)
    itens_venda = database.relationship('ItemVenda', backref='produto')

    def calcular_margem_lucro(self):

        """
        Calcula a margem de lucro do produto com base no preço de aquisição e de venda.
        """

        if self.preco != 0:
            self.margem_lucro = ((self.preco - self.preco_aquisicao) / self.preco) * 100
        else:
            self.margem_lucro = 0

    def __init__(self, produto, marca, preco_aquisicao, preco, estoque, categoria_fk):

        """
        Construtor da classe Produtos.

        Parâmetros:
            produto (str): O nome do produto.
            marca (str): A marca do produto.
            preco_aquisicao (float): O preço de aquisição do produto.
            preco (float): O preço de venda do produto.
            estoque (int): A quantidade em estoque do produto.
            categoria_fk (int): A chave estrangeira da categoria do produto.
        """

        self.produto = produto
        self.marca = marca
        self.preco_aquisicao = preco_aquisicao
        self.preco = preco
        self.estoque = estoque
        self.categoria_fk = categoria_fk
        self.calcular_margem_lucro()

    def __repr__(self):

        """
        Retorna uma representação textual do objeto Produtos.
        """

        return f'Produto({self.produto}, {self.marca}, {self.preco_aquisicao}, {self.preco}, {self.estoque}, {self.margem_lucro})'

class Categoria(database.Model):

    """
    Classe do modelo de Categoria.

    Atributos:
        id_categoria (database.Column): Coluna de chave primária para o ID da categoria.
        categoria (database.Column): Coluna para o nome da categoria.
        produtos (database.relationship): Relacionamento com a classe Produtos.

    """

    id_categoria = database.Column(database.Integer, primary_key=True)
    categoria = database.Column(database.String, nullable=False)
    produtos = database.relationship('Produtos', backref='categoria', lazy=True)

class Cliente(database.Model):

    """
    Classe do modelo de Cliente.

    Atributos:
        id_cliente (database.Column): Coluna de chave primária para o ID do cliente.
        nome (database.Column): Coluna para o nome do cliente.
        telefone (database.Column): Coluna para o telefone do cliente.
        email (database.Column): Coluna para o email do cliente.
        vendas (database.relationship): Relacionamento com a classe Venda.

    """

    id_cliente = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    telefone = database.Column(database.String)
    email = database.Column(database.String, nullable=False, unique=True)
    vendas = database.relationship('Venda', backref='cliente')

class ItemVenda(database.Model):

    """
    Classe do modelo de ItemVenda.

    Atributos:
        id_item_venda (database.Column): Coluna de chave primária para o ID do item de venda.
        produto_id (database.Column): Coluna para a chave estrangeira do ID do produto associado ao item de venda.
        venda_id (database.Column): Coluna para a chave estrangeira do ID da venda associada ao item de venda.
        quantidade (database.Column): Coluna para a quantidade do produto no item de venda.
        valor_unitario (database.Column): Coluna para o valor unitário do produto no item de venda.
        total (database.Column): Coluna para o valor total do item de venda.

    """

    id_item_venda = database.Column(database.Integer, primary_key=True)
    produto_id = database.Column(database.Integer, database.ForeignKey('produtos.id_produtos'), nullable=False)
    venda_id = database.Column(database.Integer, database.ForeignKey('venda.id_venda'), nullable=False)
    quantidade = database.Column(database.Integer, nullable=False)
    valor_unitario = database.Column(database.Float, nullable=False)
    total = database.Column(database.Float, nullable=False)

class Venda(database.Model):

    """
    Classe do modelo de Venda.

    Atributos:
        id_venda (database.Column): Coluna de chave primária para o ID da venda.
        cliente_id (database.Column): Coluna para a chave estrangeira do ID do cliente associado à venda.
        data_venda (database.Column): Coluna para a data da venda.
        itens_venda (database.relationship): Relacionamento com a classe ItemVenda.

    """

    id_venda = database.Column(database.Integer, primary_key=True)
    cliente_id = database.Column(database.Integer, database.ForeignKey('cliente.id_cliente'), nullable=False)
    data_venda = database.Column(database.Date, default=datetime.now().date, nullable=False)
    itens_venda = database.relationship('ItemVenda', backref='venda')

class Pagamento(database.Model):

    """
    Classe do modelo de Pagamento.

    Atributos:
        id_pagamento (database.Column): Coluna de chave primária para o ID do pagamento.
        metodo_pagamento (database.Column): Coluna para o método de pagamento.
        valor_pagamento (database.Column): Coluna para o valor do pagamento.
        troco (database.Column): Coluna para o valor do troco, caso aplicável.
        data_pagamento (database.Column): Coluna para a data e hora do pagamento.

    """

    id_pagamento = database.Column(database.Integer, primary_key=True)
    metodo_pagamento = database.Column(database.String, nullable=False)
    valor_pagamento = database.Column(database.Float, nullable=False)
    troco = database.Column(database.Float)
    data_pagamento = database.Column(database.DateTime, default=datetime.now, nullable=False)




