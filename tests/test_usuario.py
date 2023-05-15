import unittest
from flask import url_for
from flask_login import logout_user, login_user
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario

class TestUsuarioRout(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['SERVER_NAME'] = 'localhost:5000'
        with app.app_context():
            database.create_all()

            usuario1 = Usuario(usuario='sandoval51', email='sandoval51@gmail.com', senha=bcrypt.generate_password_hash('123456').decode('utf-8'))
            usuario2 = Usuario(usuario='sandoval52', email='sandoval52@gmail.com', senha=bcrypt.generate_password_hash('123456').decode('utf-8'))
            usuario3 = Usuario(usuario='sandoval53', email='sandoval53@gmail.com', senha=bcrypt.generate_password_hash('123456').decode('utf-8'))
            database.session.add_all([usuario1, usuario2, usuario3])
            database.session.commit()

    def test_usuario_rout(self):
        with app.test_request_context():
            user = Usuario(usuario='sandoval54', email='sandoval54@gmail.com',
                           senha=bcrypt.generate_password_hash('123456').decode('utf-8'))
            database.session.add(user)
            database.session.commit()

            response_login = self.app.post(url_for('login'), data=dict(
                usuario='sandoval54',
                senha='123456'
            ), follow_redirects=True)

            self.assertEqual(response_login.status_code, 200)

            login_user(user)

            response_usuario = self.app.get(url_for('usuarios'))

            self.assertEqual(response_usuario.status_code, 200)

            logout_user()


if __name__ == '__main__':
    unittest.main()