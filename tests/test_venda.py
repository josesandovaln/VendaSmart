import unittest
from flask import url_for
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario, Categoria, Produtos, Venda


class TestVendasRout(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['SERVER_NAME'] = 'localhost:5000'
        with app.app_context():
            database.create_all()

            user = Usuario(
                usuario='sandoval110',
                email='sandoval110@gmail.com',
                senha=bcrypt.generate_password_hash('123456').decode('utf-8')
            )
            categoria = Categoria(categoria='Categoria de Teste')
            database.session.add(user)
            database.session.add(categoria)
            database.session.commit()

            produto = Produtos(
                produto='Produto Teste',
                preco=100.0,
                estoque=10,
                categoria_fk=1
            )
            database.session.add(produto)
            database.session.commit()

    def test_venda_route(self):
        with app.app_context():
            response = self.app.post(url_for('login'), data=dict(
                usuario='sandoval110',
                senha='123456'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            response = self.app.get(url_for('vendas'), follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            produto_id = 1
            quantidade = 5
            produto = Produtos.query.filter_by(id_produtos=produto_id).first()
            if produto is None:
                self.fail('Produto não encontrado')

            if quantidade > produto.estoque:
                self.fail('Estoque insuficiente')

            total = produto.preco * quantidade
            form_data = dict(
                produto_id=produto_id,
                quantidade=quantidade,
                total=total
            )
            response = self.app.post(url_for('vendas'), data=form_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            venda = Venda(produto_id=produto_id, quantidade=quantidade, total=total)
            database.session.add(venda)
            produto.estoque -= quantidade
            database.session.commit()

            with database.session.no_autoflush:
                venda_criada = Venda.query.filter_by(produto_id=produto_id).first()
                if venda_criada is not None:
                    database.session.refresh(venda_criada)
                    self.assertEqual(venda_criada.produto_id, produto_id)
                    self.assertEqual(venda_criada.quantidade, quantidade)
                    self.assertEqual(venda_criada.total, total)
                else:
                    self.fail('Venda não encontrada')



if __name__ == '__main__':
    unittest.main()
