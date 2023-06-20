from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, SelectField, \
    DateField, TextAreaField
from wtforms.validators import DataRequired, length, email, equal_to, Length, EqualTo


class FormLogin(FlaskForm):

    """
    Classe para o formulário de login.

    Atributos:
        usuario (StringField): Campo de entrada de texto para o nome de usuário.
        senha (PasswordField): Campo de entrada de texto para a senha.
        lembrar (BooleanField): Campo de seleção para lembrar o usuário.
        submit_entrar (SubmitField): Botão de envio do formulário.

    Exemplo de uso:
        form = FormLogin()
        if form.validate_on_submit():
            # Executar ações de login
    """

    usuario = StringField('Usuário:', validators=[DataRequired(), length(5)])
    senha = PasswordField('Senha:',  validators=[DataRequired(), length(6, 16)])
    lembrar = BooleanField('Lembrar-me')
    submit_entrar = SubmitField('Entrar')

class FormCadastroUsuario(FlaskForm):

    """
    Classe para o formulário de cadastro de usuário.

    Atributos:
        usuario (StringField): Campo de entrada de texto para o nome de usuário.
        email (StringField): Campo de entrada de texto para o e-mail.
        senha (PasswordField): Campo de entrada de texto para a senha.
        confirmacao (PasswordField): Campo de entrada de texto para a confirmação da senha.
        submit_cadastro_usuario (SubmitField): Botão de envio do formulário.

    Exemplo de uso:
        form = FormCadastroUsuario()
        if form.validate_on_submit():
            # Executar ações de cadastro de usuário
    """

    usuario = StringField('Usuário:', validators=[DataRequired(), Length(min=5)])
    email = StringField('E-mail:', validators=[DataRequired(), email()])
    senha = PasswordField('Senha:',  validators=[DataRequired(), length(6, 16)])
    confirmacao = PasswordField('Confirmação da senha:',  validators=[DataRequired(), equal_to('senha')])
    submit_cadastro_usuario = SubmitField('Criar')

class FormEditarUsuario(FlaskForm):

    """
    Classe para o formulário de edição de usuário.

    Atributos:
        usuario (StringField): Campo de entrada de texto para o nome de usuário.
        email (StringField): Campo de entrada de texto para o e-mail.

    Exemplo de uso:
        form = FormEditarUsuario()
        if form.validate_on_submit():
            # Executar ações de edição de usuário
    """

    usuario = StringField('Usuário:', validators=[DataRequired(), Length(min=5)])
    email = StringField('E-mail:', validators=[DataRequired(), email()])

class FormAtualizarSenha(FlaskForm):

    """
    Classe para o formulário de atualização de senha.

    Atributos:
        senha_atual (PasswordField): Campo de entrada de texto para a senha atual.
        nova_senha (PasswordField): Campo de entrada de texto para a nova senha.
        confirmar_senha (PasswordField): Campo de entrada de texto para a confirmação da nova senha.
        submit (SubmitField): Botão de envio do formulário.

    Exemplo de uso:
        form = FormAtualizarSenha()
        if form.validate_on_submit():
            # Executar ações de atualização de senha
    """

    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('nova_senha', message='As senhas não coincidem')])
    submit = SubmitField('Atualizar Senha')

class FormListarUsuario(FlaskForm):

    """
    Classe para o formulário de listagem de usuários.

    Atributos:
        usuarios (None): Atributo vazio para a lista de usuários.
        submit_excluir_usuario (SubmitField): Botão de envio do formulário para excluir usuário.

    Exemplo de uso:
        form = FormListarUsuario()
        if form.validate_on_submit():
            # Executar ações de listagem de usuários
    """

    usuarios = None
    submit_excluir_usuario = SubmitField('Excluir')

class VendasForm(FlaskForm):

    """
    Classe para o formulário de vendas.

    Atributos:
        produto_id (IntegerField): Campo de entrada de texto para o ID do produto.
        quantidade (IntegerField): Campo de entrada de texto para a quantidade de produtos.
        submit (SubmitField): Botão de envio do formulário.

    Exemplo de uso:
        form = VendasForm()
        if form.validate_on_submit():
            # Executar ações de vendas
    """

    produto_id = IntegerField('ID do Produto', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])
    submit = SubmitField('Confirmar')

class PagamentoForm(FlaskForm):

    """
    Classe para o formulário de pagamento.

    Atributos:
        metodo_pagamento (SelectField): Campo de seleção para o método de pagamento.
        valor_pago (FloatField): Campo de entrada de texto para o valor do pagamento.
        parcelas (SelectField): Campo de seleção para o número de parcelas.
        submit (SubmitField): Botão de envio do formulário.

    Exemplo de uso:
        form = PagamentoForm()
        if form.validate_on_submit():
            # Executar ações de pagamento
    """

    metodo_pagamento = SelectField('Método de Pagamento', choices=[('dinheiro', 'Dinheiro'), ('cartao de crédito', 'Cartão de crédito'), ('cartao de débito', 'Cartão de débito'), ('pix', 'Pix')], validators=[DataRequired()])
    valor_pago = FloatField('Valor do Pagamento', validators=[DataRequired()])
    parcelas = SelectField('Número de Parcelas', choices=[
        (1, '1x'),
        (2, '2x'),
        (3, '3x'),
    ])
    submit = SubmitField('Confirmar')

class RelatorioVendasDiarioForm(FlaskForm):

    """
    Classe para o formulário de relatório de vendas diário.

    Atributos:
        data (DateField): Campo de entrada de data para selecionar a data do relatório.

    Exemplo de uso:
        form = RelatorioVendasDiarioForm()
        if form.validate_on_submit():
            # Executar ações de geração de relatório de vendas diário
    """

    data = DateField('Data', validators=[DataRequired()])

class HelpDeskForm(FlaskForm):

    """
    Classe para o formulário de Help Desk.

    Atributos:
        subject (StringField): Campo de entrada de texto para o assunto do ticket.
        description (TextAreaField): Campo de entrada de texto multilinha para a descrição do ticket.

    Exemplo de uso:
        form = HelpDeskForm()
        if form.validate_on_submit():
            # Executar ações de criação do ticket de Help Desk
    """

    subject = StringField('Assunto', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])