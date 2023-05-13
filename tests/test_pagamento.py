import unittest
from flask import url_for
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario, Categoria, Produtos, Pagamento

class TestPagamentoRout(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['SERVER_NAME'] = 'localhost:5000'
        with app.app_context():
            database.create_all()


            user = Usuario(
                usuario='sandoval90',
                email='sandoval90@gmail.com',
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

    def test_pagamento_route(self):
        with app.app_context():
            response = self.app.post(url_for('login'), data=dict(
                usuario='sandoval90',
                senha='123456'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            response = self.app.get(url_for('pagamento'), follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            form_data = dict(
                metodo_pagamento='dinheiro',
                valor_pago=150.0
            )
            response = self.app.post(url_for('pagamento'), data=form_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            with database.session.no_autoflush:
                pagamento_criado = Pagamento.query.filter_by(metodo_pagamento='dinheiro').first()
                if pagamento_criado is not None:
                    database.session.refresh(pagamento_criado)
                    self.assertEqual(pagamento_criado.metodo_pagamento, 'dinheiro')
                    self.assertEqual(pagamento_criado.valor_pagamento, 115.98)
                    # calculate change
                    self.assertEqual(pagamento_criado.troco, 0.0)
                else:
                    self.fail('Pagamento não encontrado')



if __name__ == '__main__':
    unittest.main()
