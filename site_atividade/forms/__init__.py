from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, length, email, equal_to

class FormLogin(FlaskForm):
    usuario = StringField('Usuário:', validators=[DataRequired(), length(5)])
    senha = PasswordField('Senha:',  validators=[DataRequired(), length(6, 16)])
    lembrar = BooleanField('Lembrar-me')
    submit_entrar = SubmitField('Entrar')

class FormCadastroUsuario(FlaskForm):
    usuario = StringField('Usuário:', validators=[DataRequired(), length(5)])
    email = StringField('E-mail:', validators=[DataRequired(), email()])
    senha = PasswordField('Senha:',  validators=[DataRequired(), length(6, 16)])
    confirmacao = PasswordField('Confirmação da senha:',  validators=[DataRequired(), equal_to('senha')])
    submit_cadastro_usuario = SubmitField('Criar')

class FormListarUsuario(FlaskForm):
    usuarios = None
    submit_excluir_usuario = SubmitField('Excluir')

class VendasForm(FlaskForm):
    produto_id = IntegerField('ID do Produto', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])
    submit = SubmitField('Confirmar')

class PagamentoForm(FlaskForm):
    metodo_pagamento = SelectField('Método de Pagamento', choices=[('dinheiro', 'Dinheiro'), ('cartao de crédito', 'Cartão de crédito'), ('cartao de débito', 'Cartão de débito'), ('pix', 'Pix')], validators=[DataRequired()])
    valor_pago = FloatField('Valor do Pagamento', validators=[DataRequired()])
    submit = SubmitField('Confirmar')