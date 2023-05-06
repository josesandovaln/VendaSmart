from datetime import datetime
from flask import render_template, url_for, redirect, flash, request
from site_atividade.forms import FormLogin, FormCadastroUsuario, FormListarUsuario, VendasForm, PagamentoForm
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario, Produtos, Categoria, Venda, Pagamento
from flask_login import login_user, logout_user, login_required


@app.route("/", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        user = Usuario.query.filter_by(usuario=form_login.usuario.data).first()
        if user and bcrypt.check_password_hash(user.senha, form_login.senha.data):
            login_user(user, remember=form_login.lembrar.data)
            flash(f'Login feito com sucesso para usuario: {form_login.usuario.data}', 'alert-success')
            return redirect(url_for('produtos'))
        else:
            flash(f'Usuário ou senha incorretos', 'alert-danger')
            return redirect(url_for('login'))
    return render_template('login.html', form_login=form_login)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão finalizada', 'alert-info')
    return redirect(url_for('login'))

@app.route("/produtos")
@login_required
def produtos():
    produtos = Produtos.query.all()
    return render_template('lista_produto.html', produtos=produtos)

@app.route("/delete-produto/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_produto(id):
    produto = Produtos.query.get(id)
    if request.method == 'POST':
        if produto:
            database.session.delete(produto)
            database.session.commit()
            flash(f'Produto "{produto.produto}" excluído com sucesso', 'alert-success')
        else:
            flash(f'Produto não encontrado', 'alert-danger')
        return redirect(url_for('produtos'))
    return render_template('delete_produto.html', produto=produto)

@app.route('/novo-produto', methods=['GET', 'POST'])
@login_required
def novo_produto():
    if request.method == 'POST':
        produto = Produtos(
            produto=request.form['produto'],
            preco=float(request.form['preco']),
            estoque=int(request.form['estoque']),
            categoria_fk=int(request.form['categoria_fk'])
        )
        database.session.add(produto)
        database.session.commit()
        flash(f'O produto {produto.produto} foi criado com sucesso!', 'alert-success')
        return redirect(url_for('produtos'))

    categorias = Categoria.query.all()
    return render_template('novo_produto.html', categorias=categorias)

@app.route("/editar-produto/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produtos.query.get(id)
    if request.method == 'POST':
        produto.produto = request.form['produto']
        produto.preco = float(request.form['preco'])
        produto.estoque = int(request.form['estoque'])
        produto.categoria_fk = int(request.form['categoria_fk'])
        database.session.commit()
        flash(f'Produto "{produto.produto}" editado com sucesso', 'alert-success')
        return redirect(url_for('produtos'))
    categorias = Categoria.query.all()
    return render_template('editar_produto.html', produto=produto, categorias=categorias)


@app.route("/cadastro-usuario", methods=['GET', 'POST'])
@login_required
def cadastro_usuario():
    form_cadastro_usuario = FormCadastroUsuario()
    if form_cadastro_usuario.validate_on_submit():
        try:
            user = Usuario(usuario=form_cadastro_usuario.usuario.data, email=form_cadastro_usuario.email.data, senha=form_cadastro_usuario.senha.data)
            database.session.add(user)
            database.session.commit()
            flash(f'Usuario {user.usuario} cadastrado com sucesso', 'alert-success')
        except:
            flash(f'Falha ao cadastrar usuário - Usuário já existe', 'alert-danger')
        return redirect(url_for('cadastro_usuario'))
    return render_template("cadastrar_usuario.html", form_cadastro_usuario=form_cadastro_usuario)


@app.route("/vendas", methods=['GET', 'POST'])
@login_required
def vendas():
    form = VendasForm(request.form)
    produtos = Produtos.query.all()

    if request.method == 'POST' and form.validate():
        produto_id = form.produto_id.data
        quantidade = form.quantidade.data

        produto = Produtos.query.get(produto_id)

        if produto is None:
            flash('Produto não encontrado', 'danger')
        elif produto.estoque < quantidade:
            flash('Estoque insuficiente', 'danger')
        else:
            venda = Venda(produto_id=produto_id, quantidade=quantidade)
            venda.total = produto.preco * quantidade
            database.session.add(venda)
            produto.estoque -= quantidade
            database.session.commit()

            return redirect(url_for('vendas'))

    vendas = Venda.query.all()

    if request.method == 'POST' and 'LimparVendas' in request.form:
        Venda.query.delete()
        database.session.commit()

        return redirect(url_for('vendas'))

    return render_template('vendas.html', form=form, produtos=produtos, vendas=vendas)

@app.route('/pagamento', methods=['GET', 'POST'])
@login_required
def pagamento():
    vendas = Venda.query.all()
    total = sum([venda.total for venda in vendas])

    form = PagamentoForm()

    if form.validate_on_submit():
        metodo_pagamento = form.metodo_pagamento.data
        valor_pago = form.valor_pago.data

        if not valor_pago:
            return render_template('pagamento.html', erro='Valor de pagamento é obrigatório.', metodo_pagamento=metodo_pagamento, total=total)

        valor_pago = float(valor_pago)

        troco = valor_pago - total if valor_pago >= total else 0

        return render_template('pagamento.html', metodo_pagamento=metodo_pagamento, total=total, valor_pago=valor_pago, troco=troco)

    return render_template('pagamento.html', form=form, total=total)

@app.route('/confirmar_pagamento', methods=['POST'])
@login_required
def confirmar_pagamento():
    form = PagamentoForm()
    total = sum([venda.total for venda in Venda.query.all()])

    if form.validate_on_submit():
        metodo_pagamento = form.metodo_pagamento.data
        valor_pago = form.valor_pago.data
        total = sum([venda.total for venda in Venda.query.all()])

        if valor_pago < total:
            return render_template('pagamento.html', erro='Valor de pagamento insuficiente.', form=form, total=total)

        troco = valor_pago - total

        pagamento = Pagamento(metodo_pagamento=metodo_pagamento, valor_pagamento=valor_pago, troco=troco, data_pagamento=datetime.now())

        database.session.add(pagamento)
        database.session.commit()

        database.session.query(Venda).delete()
        database.session.commit()

        return render_template('confirmacao_pagamento.html', pagamento=pagamento)

    return render_template('pagamento.html', form=form, total=total)









