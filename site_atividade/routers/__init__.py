from datetime import datetime

import mail
from flask import render_template, url_for, redirect, flash, request, get_template_attribute, jsonify, \
    render_template_string, current_app, session
from flask_mail import Message

from sqlalchemy import desc

from site_atividade.forms import FormLogin, FormCadastroUsuario, FormListarUsuario, VendasForm, PagamentoForm, \
    FormEditarUsuario, FormAtualizarSenha, HelpDeskForm
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario, Produtos, Categoria, Venda, Pagamento, ItemVenda, Cliente
from flask_login import login_user, logout_user, login_required

import plotly.graph_objects as go
from plotly.subplots import make_subplots



@app.route("/", methods=['GET', 'POST'])
def login():

    """
    Rota para a página de login.

    - GET: Exibe o formulário de login.
    - POST: Valida os dados de login e redireciona para a página de produtos em caso de sucesso.
    """

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

    """
    Rota para encerrar a sessão do usuário.

    - GET: Encerra a sessão do usuário atualmente logado e redireciona para a página de login.
    """

    logout_user()
    flash('Sessão finalizada', 'alert-info')

    return redirect(url_for('login'))

@app.route("/produtos")
@login_required
def produtos():

    """
    Rota para exibir a lista de produtos.

    - GET: Exibe a lista de produtos com base nos parâmetros de pesquisa fornecidos.
    """

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

    """
    Rota para adicionar uma nova categoria.

    - POST: Adiciona uma nova categoria com base nos dados enviados pelo formulário.
    """

    categoria = request.form.get('categoria')
    nova_categoria = Categoria(categoria=categoria)
    database.session.add(nova_categoria)
    database.session.commit()

    flash('Nova categoria adicionada com sucesso!', 'alert-success')

    return redirect(url_for('produtos'))

@app.route("/delete-produto/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_produto(id):

    """
    Rota para excluir um produto.

    - GET: Exibe a página de confirmação de exclusão do produto.
    - POST: Exclui o produto do banco de dados.
    """

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

    """
    Rota para adicionar um novo produto.

    - GET: Exibe o formulário para adicionar um novo produto.
    - POST: Valida os dados do formulário e adiciona o novo produto ao banco de dados.
    """

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

    """
    Rota para editar um produto existente.

    - GET: Exibe o formulário preenchido com os dados do produto a ser editado.
    - POST: Valida e salva as alterações feitas no produto.
    """

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

    """
    Rota para cadastrar um novo usuário.

    - GET: Exibe o formulário de cadastro de usuário.
    - POST: Valida os dados do formulário e cadastra o novo usuário no banco de dados.
    """

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

    """
    Rota para exibir a lista de usuários.

    - GET: Exibe a lista de usuários cadastrados.
    """

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

    """
    Rota para excluir um usuário.

    - GET: Exibe a página de confirmação de exclusão do usuário.
    - POST: Exclui o usuário do banco de dados.
    """

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

    """
    Rota para editar um usuário existente.

    - GET: Exibe o formulário preenchido com os dados do usuário para edição.
    - POST: Atualiza os dados do usuário no banco de dados.
    """

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

    """
    Rota para atualizar a senha de um usuário.

    - GET: Exibe o formulário para atualização da senha.
    - POST: Verifica a senha atual e atualiza a senha do usuário no banco de dados.
    """

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

    """
    Rota para gerenciar as vendas.

    - GET: Exibe a página de vendas com a lista de clientes, produtos e vendas.
    - POST: Limpa todas as vendas realizadas, removendo os itens de venda do banco de dados.
    """

    search_query = request.args.get('search', '')

    clientes = Cliente.query.all()
    produtos = Produtos.query.filter(Produtos.produto.ilike(f'%{search_query}%')).all()
    vendas = Venda.query.all()

    if request.method == 'POST' and 'LimparVendas' in request.form:
        ItemVenda.query.delete()
        database.session.commit()

        return redirect(url_for('vendas'))

    return render_template('vendas.html', clientes=clientes, produtos=produtos, vendas=vendas, search_query=search_query)

@app.route("/adicionar_venda", methods=['POST'])
@login_required
def adicionar_venda():

    """
    Rota para adicionar uma nova venda.

    - POST: Obtém o ID do cliente selecionado, cria uma nova venda associada a esse cliente e salva no banco de dados.
    Retorna um JSON indicando se a operação foi bem-sucedida ou não.
    """
    
    cliente_id = request.form.get('cliente_id')
    cliente = Cliente.query.get(cliente_id)

    if cliente is None:
        return jsonify({'success': False, 'message': 'Cliente não encontrado'})

    venda = Venda(cliente_id=cliente_id, data_venda=datetime.now().date())
    database.session.add(venda)
    database.session.commit()

    return jsonify({'success': True})

@app.route("/adicionar_item_venda", methods=['POST'])
@login_required
def adicionar_item_venda():

    """
    Rota para adicionar um novo item de venda.

    - POST: Obtém o ID do produto e a quantidade do item de venda a ser adicionado.
    Verifica se o produto existe e se há estoque suficiente.
    Cria um novo item de venda associado à venda atual, atualiza o estoque do produto e salva as alterações no banco de dados.
    Retorna um JSON indicando se a operação foi bem-sucedida ou não, juntamente com o HTML atualizado das vendas.
    """

    produto_id = request.form.get('produto_id')
    quantidade = int(request.form.get('quantidade'))

    produto = Produtos.query.get(produto_id)

    if produto is None:
        return jsonify({'success': False, 'message': 'Produto não encontrado'})
    elif produto.estoque < quantidade:
        return jsonify({'success': False, 'message': 'Estoque insuficiente'})

    venda = Venda.query.order_by(Venda.id_venda.desc()).first()
    item_venda = ItemVenda(produto_id=produto_id, venda_id=venda.id_venda, quantidade=quantidade, valor_unitario=produto.preco, total=produto.preco * quantidade)
    database.session.add(item_venda)
    produto.estoque -= quantidade
    database.session.commit()

    venda = Venda.query.order_by(Venda.id_venda.desc()).first()

    vendas_html = render_template_string('{% for item_venda in venda.itens_venda %}<tr><td class="text-center">{{ item_venda.produto.id_produtos }}</td><td class="text-center">{{ item_venda.produto.produto }}</td><td class="text-center">{{ item_venda.produto.marca }}</td><td class="text-center">{{ "{:.2f}".format(item_venda.produto.preco).replace(".", ",") }}</td><td class="text-center">{{ item_venda.quantidade }}</td><td class="text-center">{{ "{:.2f}".format(item_venda.total).replace(".", ",") }}</td></tr>{% endfor %}', venda=venda)

    return jsonify({'success': True, 'vendas_html': vendas_html})

@app.route("/pagamento", methods=['GET', 'POST'])
@login_required
def pagamento():

    """
    Rota para processar o pagamento de uma venda.

    - GET: Obtém todas as vendas no banco de dados e calcula o total das vendas.
    Renderiza o formulário de pagamento, exibindo o total a ser pago.

    - POST: Obtém os dados do formulário de pagamento submetido.
    Valida os campos do formulário e processa o pagamento.
    Calcula o troco, se aplicável, e renderiza a página de pagamento com os detalhes do pagamento.
    """

    vendas = Venda.query.all()
    total = sum([item_venda.total for venda in vendas for item_venda in venda.itens_venda])

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

@app.route("/confirmar_pagamento", methods=['GET', 'POST'])
@login_required
def confirmar_pagamento():

    """
    Rota para confirmar o pagamento de uma venda.

    - GET: Obtém todas as vendas no banco de dados e calcula o total das vendas.
    Renderiza o formulário de pagamento, exibindo o total a ser pago.

    - POST: Obtém os dados do formulário de pagamento submetido.
    Valida os campos do formulário e confirma o pagamento.
    Calcula o troco, se aplicável, e renderiza a página de confirmação de pagamento.
    """

    form = PagamentoForm()
    vendas = Venda.query.all()
    total = sum([item_venda.total for venda in vendas for item_venda in venda.itens_venda])

    if form.validate_on_submit():
        metodo_pagamento = form.metodo_pagamento.data
        valor_pago = form.valor_pago.data
        total = sum([item_venda.total for venda in vendas for item_venda in venda.itens_venda])

        if valor_pago < total:
            return render_template('pagamento.html', erro='Valor de pagamento insuficiente.', form=form, total=total)

        troco = valor_pago - total

        pagamento = Pagamento(metodo_pagamento=metodo_pagamento, valor_pagamento=valor_pago, troco=troco,
                              data_pagamento=datetime.now())

        database.session.add(pagamento)
        database.session.commit()

        return render_template('confirmacao_pagamento.html', pagamento=pagamento, total=total)

    return render_template('pagamento.html', form=form, total=total)

@app.route("/obter_ultimo_pagamento", methods=['GET'])
@login_required
def obter_ultimo_pagamento():

    """
    Rota para obter as informações do último pagamento registrado.

    - GET: Obtém o último pagamento registrado no banco de dados.
    Verifica se existe um último pagamento e retorna as informações em formato JSON.
    Caso não haja último pagamento, retorna um objeto vazio em formato JSON.
    """

    ultimo_pagamento = Pagamento.query.order_by(desc(Pagamento.id_pagamento)).first()

    if ultimo_pagamento:
        vendas = Venda.query.all()
        valor_total_vendas = sum([item_venda.total for venda in vendas for item_venda in venda.itens_venda])
        troco = ultimo_pagamento.troco

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
        return jsonify(ultimo_pagamento={})

@app.route("/clientes")
@login_required
def clientes():

    """
    Rota para exibir a lista de clientes.

    - GET: Obtém a lista de clientes do banco de dados.
    Aceita um parâmetro de pesquisa opcional para filtrar os clientes por nome.
    Renderiza o template 'lista_cliente.html' e passa a lista de clientes como contexto.
    """

    search_term = request.args.get('search')

    if search_term:
        clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{search_term}%')).all()
    else:
        clientes = Cliente.query.all()

    return render_template('lista_cliente.html', clientes=clientes)

@app.route('/novo-cliente', methods=['GET', 'POST'])
@login_required
def novo_cliente():

    """
    Rota para adicionar um novo cliente.

    - GET: Renderiza o template 'novo_cliente.html' para exibir o formulário de criação de cliente.
    - POST: Processa os dados enviados pelo formulário de criação de cliente.
    Cria um novo objeto Cliente com os dados fornecidos.
    Adiciona o objeto Cliente ao banco de dados e faz o commit.
    Exibe uma mensagem de sucesso usando flash.
    Redireciona para a rota 'clientes' após a criação do cliente.
    """

    if request.method == 'POST':
        cliente = Cliente(
            nome=request.form['nome'],
            telefone=request.form['telefone'],
            email=request.form['email']
        )
        database.session.add(cliente)
        database.session.commit()
        flash(f'O cliente {cliente.nome} foi criado com sucesso!', 'alert-success')
        return redirect(url_for('clientes'))

    return render_template('novo_cliente.html')

@app.route("/editar-cliente/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_cliente(id):

    """
    Rota para editar um cliente existente.

    - GET: Renderiza o template 'editar_cliente.html' preenchido com os dados do cliente a ser editado.
    - POST: Processa os dados enviados pelo formulário de edição de cliente.
    Atualiza o objeto Cliente com os novos dados fornecidos.
    Faz o commit das alterações no banco de dados.
    Exibe uma mensagem de sucesso usando flash.
    Redireciona para a rota 'clientes' após a edição do cliente.
    """

    cliente = Cliente.query.get(id)

    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.telefone = request.form['telefone']
        cliente.email = request.form['email']
        database.session.commit()
        flash(f'Cliente "{cliente.nome}" editado com sucesso', 'alert-success')
        return redirect(url_for('clientes'))

    return render_template('editar_cliente.html', cliente=cliente)

@app.route("/delete-cliente/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_cliente(id):

    """
    Rota para excluir um cliente.

    - GET: Renderiza o template 'delete_cliente.html' com os dados do cliente a ser excluído.
    - POST: Processa a exclusão do cliente.
    Verifica se o cliente existe no banco de dados.
    Se existir, remove o cliente do banco de dados e faz o commit das alterações.
    Exibe uma mensagem de sucesso usando flash.
    Redireciona para a rota 'clientes' após a exclusão do cliente.
    """

    cliente = Cliente.query.get(id)

    if request.method == 'POST':
        if cliente:
            database.session.delete(cliente)
            database.session.commit()
            flash(f'Cliente "{cliente.nome}" excluído com sucesso', 'alert-success')
        else:
            flash(f'Cliente não encontrado', 'alert-danger')

        return redirect(url_for('clientes'))

    return render_template('delete_cliente.html', cliente=cliente)

@app.route('/helpdesk', methods=['GET', 'POST'])
@login_required
def helpdesk():

    """
    Rota para o formulário de solicitação de suporte.

    - GET: Renderiza o template 'helpdesk.html' com o formulário vazio.
    - POST: Processa o envio da solicitação de suporte.
    Verifica se o formulário foi preenchido corretamente.
    Obtém o assunto e a descrição da solicitação de suporte.
    Executa a lógica para enviar a solicitação aos desenvolvedores (exemplo: envio de e-mail).
    Exibe uma mensagem de sucesso usando flash.
    Redireciona para a rota 'helpdesk' após o envio da solicitação.
    """

    form = HelpDeskForm()

    if form.validate_on_submit():
        subject = form.subject.data
        description = form.description.data
        send_support_request_email(subject, description)

        flash('Sua solicitação de suporte foi enviada com sucesso!', 'alert-success')

        return redirect(url_for('helpdesk'))

    return render_template('helpdesk.html', form=form)

def send_support_request_email(subject, description):

    """
    Função para enviar a solicitação de suporte por e-mail aos desenvolvedores.

    - Parâmetros:
        - subject: Assunto da solicitação de suporte.
        - description: Descrição da solicitação de suporte.
    """

    message = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], recipients=[current_app.config['SUPPORT_EMAIL']])
    message.body = description
    mail.send(message)

@app.route("/relatorio_vendas_diario")
@login_required
def relatorio_vendas_diario():

    """
    Renderiza o gráfico de barras.

    - Parâmetros:
        - produtos: Lista de nomes dos produtos vendidos.
        - quantidades: Lista de quantidades vendidas de cada produto.
        - valores_totais: Lista de valores totais de venda de cada produto.
        - valor_total_vendas: Valor total de vendas no dia.

    - Retorna:
        - graph_html: O gráfico de barras renderizado em HTML.
    """

    data_selecionada = request.args.get('data')
    
    if data_selecionada:
        data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
        vendas = Venda.query.filter(Venda.data_venda == data_selecionada).all()

        produtos = []
        quantidades = []
        valores_totais = []
        for venda in vendas:
            for item_venda in venda.itens_venda:
                produtos.append(item_venda.produto.produto)
                quantidades.append(item_venda.quantidade)
                valores_totais.append(item_venda.total)
        
        valor_total_vendas = sum(valores_totais)

        fig = go.Figure(data=[go.Bar(x=produtos, y=quantidades, text=valores_totais, textposition='auto', marker=dict(color='#DC236D'))])

        fig.update_layout(
                          xaxis_title="Produto",
                          yaxis_title="Quantidade Vendida")
        
        fig.add_annotation(xref='x', yref='paper', x=0.0, y=-0.07,
                       text=f"<b>Total Vendas: R$ {valor_total_vendas:.2f}</b>",
                       showarrow=False,
                       font=dict(color='black', size=16),  # Aumente o tamanho da fonte aqui
                       xanchor='center')
        
        graph_html = fig.to_html(full_html=False)
        
        return render_template('relatorio_vendas_diario.html', vendas=vendas, data_atual=data_selecionada, graph_html=graph_html)
    
    return render_template('relatorio_vendas_diario.html')








