import unittest
from flask import url_for
from flask_login import logout_user, login_user
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario, Produtos

class TestProdutosRout(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['SERVER_NAME'] = 'localhost:5000'
        with app.app_context():
            database.create_all()

            produto1 = Produtos(produto='Macarrão', preco=6.90, estoque=30, categoria_fk=1)
            produto2 = Produtos(produto='Água', preco=1.0, estoque=50, categoria_fk=3)
            produto3 = Produtos(produto='Energético', preco=1.0, estoque=50, categoria_fk=3)
            database.session.add_all([produto1, produto2, produto3])
            database.session.commit()

    def test_produtos_rout_authenticated(self):
        with app.test_request_context():
            user = Usuario(usuario='sandoval100', email='sandoval100@gmail.com',
                           senha=bcrypt.generate_password_hash('123456').decode('utf-8'))
            database.session.add(user)
            database.session.commit()

            response_login = self.app.post(url_for('login'), data=dict(
                usuario='sandoval100',
                senha='123456'
            ), follow_redirects=True)

            self.assertEqual(response_login.status_code, 200)

            login_user(user)

            response_produtos = self.app.get(url_for('produtos'))

            self.assertEqual(response_produtos.status_code, 200)

            logout_user()

    def test_produtos_rout_unauthenticated(self):
        with app.test_request_context():
            # Acessa a rota "/produtos" sem estar autenticado
            response = self.app.get(url_for('produtos'))

            # Verifica se o redirecionamento para a página de login ocorreu com sucesso
            self.assertEqual(response.status_code, 302)



if __name__ == '__main__':
    unittest.main()


