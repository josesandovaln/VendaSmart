from datetime import datetime

import mail
from flask import render_template, url_for, redirect, flash, request, get_template_attribute, jsonify, \
    render_template_string, current_app
from flask_mail import Message
from sqlalchemy import desc

from site_atividade.forms import FormLogin, FormCadastroUsuario, FormListarUsuario, VendasForm, PagamentoForm, \
    FormEditarUsuario, FormAtualizarSenha, HelpDeskForm
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
    search_term = request.args.get('search')

    if search_term:
        produtos = Produtos.query.filter(Produtos.produto.ilike(f'%{search_term}%')).all()
    else:
        produtos = Produtos.query.all()

    categorias = Categoria.query.all()  # Obter todas as categorias

    return render_template('lista_produto.html', produtos=produtos, categorias=categorias)

@app.route('/nova-categoria', methods=['POST'])
@login_required
def nova_categoria():
    categoria = request.form.get('categoria')
    nova_categoria = Categoria(categoria=categoria)
    database.session.add(nova_categoria)
    database.session.commit()
    flash('Nova categoria adicionada com sucesso!', 'alert-success')
    return redirect(url_for('produtos'))

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
        preco = float(request.form['preco'])
        preco_aquisicao = float(request.form['preco_aquisicao'])
        estoque = int(request.form['estoque'])

        if preco <= 0 or estoque <= 0:
            flash('O preço e o estoque devem ser maiores do que 0.', 'alert-danger')
        else:
            produto = Produtos(
                produto=request.form['produto'],
                marca=request.form['marca'],
                preco_aquisicao=preco_aquisicao,
                preco=preco,
                estoque=estoque,
                categoria_fk=int(request.form['categoria_fk'])
            )
            produto.calcular_margem_lucro()
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
        produto.marca = request.form['marca']
        if float(request.form['preco_aquisicao']) <= 0:
            flash('O preço de aquisição deve ser maior do que zero', 'alert-danger')
            return redirect(url_for('editar_produto', id=id))
        produto.preco_aquisicao = float(request.form['preco_aquisicao'])
        if float(request.form['preco']) <= 0:
            flash('O preço deve ser maior do que zero', 'alert-danger')
            return redirect(url_for('editar_produto', id=id))
        produto.preco = float(request.form['preco'])
        if int(request.form['estoque']) <= 0:
            flash('O estoque deve ser maior do que zero', 'alert-danger')
            return redirect(url_for('editar_produto', id=id))
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
            senha_crypto = bcrypt.generate_password_hash(form_cadastro_usuario.senha.data)
            user = Usuario(usuario=form_cadastro_usuario.usuario.data, email=form_cadastro_usuario.email.data,
                           senha=senha_crypto)
            database.session.add(user)
            database.session.commit()
            flash(f'Usuário {user.usuario} cadastrado com sucesso', 'alert-success')
            return redirect(url_for('usuarios'))
        except:
            flash(f'Falha ao cadastrar usuário - Usuário já existe', 'alert-danger')

    if form_cadastro_usuario.senha.data != form_cadastro_usuario.confirmacao.data:
        flash('As senhas não correspondem.', 'alert-danger')

    return redirect(url_for('usuarios'))

@app.route("/usuarios")
@login_required
def usuarios():
    form_cadastro_usuario = FormCadastroUsuario()
    form_editar_usuario = FormEditarUsuario()
    form = FormAtualizarSenha()
    search_query = request.args.get('search')
    if search_query:
        usuarios = Usuario.query.filter(Usuario.usuario.ilike(f"%{search_query}%")).all()
    else:
        usuarios = Usuario.query.all()
    return render_template('lista_usuario.html', usuarios=usuarios, form_cadastro_usuario=form_cadastro_usuario, form_editar_usuario=form_editar_usuario, search_query=search_query, form=form)


@app.route("/delete-usuario/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_usuario(id):
    usuarios = Usuario.query.get(id)
    if request.method == 'POST':
        if usuarios:
            database.session.delete(usuarios)
            database.session.commit()
            flash(f'Usuário "{usuarios.usuario}" excluído com sucesso', 'alert-success')
        else:
            flash(f'Usuário não encontrado', 'alert-danger')
        return redirect(url_for('usuarios'))
    return render_template('delete_usuario.html', usuarios=usuarios)


@app.route("/editar-usuario/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    form_editar_usuario = FormEditarUsuario(obj=usuario)

    if request.method == 'POST':
        if form_editar_usuario.validate_on_submit():
            usuario.usuario = form_editar_usuario.usuario.data
            usuario.email = form_editar_usuario.email.data
            database.session.commit()
            flash(f'Usuário "{usuario.usuario}" atualizado com sucesso', 'alert-success')
            return redirect(url_for('usuarios'))

    return render_template('editar_usuario.html', form_editar_usuario=form_editar_usuario, usuario=usuario)

@app.route("/atualizar_senha/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar_senha(id):
    usuario = Usuario.query.get_or_404(id)
    form = FormAtualizarSenha()

    if form.validate_on_submit():
        senha_atual = form.senha_atual.data
        nova_senha = form.nova_senha.data
        confirmar_senha = form.confirmar_senha.data

        if not usuario.verificar_senha(senha_atual):
            flash('Senha atual incorreta.', 'danger')
        elif nova_senha != confirmar_senha:
            flash('A nova senha e a confirmação da senha não coincidem.', 'alert-danger')
        else:
            usuario.set_senha(nova_senha)
            database.session.commit()
            flash('Senha atualizada com sucesso.', 'alert-success')
            return redirect(url_for('usuarios'))

    return redirect(url_for('usuarios'))



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
            flash('Produto não encontrado', 'alert-danger')
        elif produto.estoque < quantidade:
            flash('Estoque insuficiente', 'alert-danger')
        else:
            venda = Venda(produto_id=produto_id, quantidade=quantidade)
            venda.total = produto.preco * quantidade
            database.session.add(venda)
            produto.estoque -= quantidade
            database.session.commit()

            vendas = Venda.query.all()

            return render_template('vendas.html', form=form, produtos=produtos, vendas=vendas)

    vendas = Venda.query.all()

    if request.method == 'POST' and 'LimparVendas' in request.form:
        Venda.query.delete()
        database.session.commit()

        return redirect(url_for('vendas'))

    return render_template('vendas.html', form=form, produtos=produtos, vendas=vendas)


@app.route("/adicionar_venda", methods=['POST'])
@login_required
def adicionar_venda():
    produto_id = request.form.get('produto_id')
    quantidade = request.form.get('quantidade')

    produto = Produtos.query.get(produto_id)

    if produto is None:
        return jsonify({'success': False, 'message': 'Produto não encontrado'})
    elif produto.estoque < int(quantidade):
        return jsonify({'success': False, 'message': 'Estoque insuficiente'})

    venda = Venda(produto_id=produto_id, quantidade=int(quantidade))
    venda.total = produto.preco * int(quantidade)
    database.session.add(venda)
    produto.estoque -= int(quantidade)
    database.session.commit()

    vendas = Venda.query.all()
    vendas_html = render_template_string('{% for venda in vendas %}<tr><td class="text-center">{{ venda.produto.id_produtos }}</td><td class="text-center">{{ venda.produto.produto }}</td><td class="text-center">{{ venda.produto.marca }}</td><td class="text-center">{{ "{:.2f}".format(venda.produto.preco).replace(".", ",") }}</td><td class="text-center">{{ venda.quantidade }}</td><td class="text-center">{{ "{:.2f}".format(venda.total).replace(".", ",") }}</td></tr>{% endfor %}', vendas=vendas)

    return jsonify({'success': True, 'vendas_html': vendas_html})







@app.route('/pagamento', methods=['GET', 'POST'])
@login_required
def pagamento():
    vendas = Venda.query.all()
    total = sum([venda.total for venda in vendas])

    form = PagamentoForm()

    if form.validate_on_submit():
        metodo_pagamento = form.metodo_pagamento.data
        valor_pago = form.valor_pago.data.replace('.', ',')
        parcelas = form.parcelas.data if form.metodo_pagamento.data == 'cartao_de_credito' else None

        if not valor_pago:
            return render_template('pagamento.html', erro='Valor de pagamento é obrigatório.', metodo_pagamento=metodo_pagamento, total=total)

        valor_pago = float(valor_pago)

        troco = valor_pago - total if valor_pago >= total else 0

        return render_template('pagamento.html', metodo_pagamento=metodo_pagamento, total=total, valor_pago=valor_pago, troco=troco, parcelas=parcelas)

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

        pagamento = Pagamento(metodo_pagamento=metodo_pagamento, valor_pagamento=valor_pago, troco=troco,
                              data_pagamento=datetime.now())

        database.session.add(pagamento)
        database.session.commit()

        database.session.query(Venda).delete()
        database.session.commit()

        return render_template('confirmacao_pagamento.html', pagamento=pagamento)

    return render_template('pagamento.html', form=form, total=total)




@app.route('/obter_ultimo_pagamento', methods=['GET'])
@login_required
def obter_ultimo_pagamento():
    ultimo_pagamento = Pagamento.query.order_by(desc(Pagamento.id_pagamento)).first()

    # Verifica se existe um último pagamento
    if ultimo_pagamento:
        valor_total_vendas = sum([venda.total for venda in Venda.query.all()])
        troco = ultimo_pagamento.troco

        # Cria um dicionário com as informações do último pagamento
        ultimo_pagamento_dict = {
            'id_pagamento': ultimo_pagamento.id_pagamento,
            'metodo_pagamento': ultimo_pagamento.metodo_pagamento,
            'valor_pagamento': ultimo_pagamento.valor_pagamento,
            'troco': troco,
            'valor_total_vendas': valor_total_vendas,  # Adiciona o valor total das vendas
            'data_pagamento': ultimo_pagamento.data_pagamento.strftime("%d/%m/%Y %H:%M:%S")
        }

        return jsonify(ultimo_pagamento=ultimo_pagamento_dict)
    else:
        # Retorna um objeto vazio se não houver último pagamento
        return jsonify(ultimo_pagamento={})


@app.route('/helpdesk', methods=['GET', 'POST'])
@login_required
def helpdesk():
    form = HelpDeskForm()

    if form.validate_on_submit():
        # Lógica para enviar a solicitação de suporte aos desenvolvedores
        subject = form.subject.data
        description = form.description.data

        # Exemplo: enviar um email para os desenvolvedores com os detalhes da solicitação
        send_support_request_email(subject, description)

        flash('Sua solicitação de suporte foi enviada com sucesso!', 'alert-success')
        return redirect(url_for('helpdesk'))

    return render_template('helpdesk.html', form=form)

def send_support_request_email(subject, description):
    # Crie uma instância da classe Message do Flask-Mail
    message = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], recipients=[current_app.config['SUPPORT_EMAIL']])
    
    # Defina o corpo do email
    message.body = description
    
    # Envie o email utilizando o objeto Mail e a função send() do Flask-Mail
    mail.send(message)








@app.route("/relatorio_vendas_diario")
@login_required
def relatorio_vendas_diario():
    data_atual = datetime.now().date()
    vendas = Venda.query.filter(Venda.data_venda == data_atual).all()

    return render_template('relatorio_vendas_diario.html', vendas=vendas, data_atual=data_atual)



