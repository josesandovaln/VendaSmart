import unittest
from flask import url_for
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario

class TesteDeleteUsuario(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['SERVER_NAME'] = 'localhost:5000'
        with app.app_context():
            database.create_all()

    def test_excluir_usuario(self):
        with app.test_request_context():
            usuario_criado = Usuario(usuario='sandoval41', email='sandoval41@gmail.com', senha=bcrypt.generate_password_hash('123456').decode('utf-8'))
            database.session.add(usuario_criado)
            database.session.commit()

            self.app.post('/login', data=dict(usuario='sandoval41', senha='123456'), follow_redirects=True)

            response = self.app.post(url_for('delete_usuario', id=usuario_criado.id), follow_redirects=True)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()