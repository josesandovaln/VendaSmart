import unittest
from flask import url_for
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario

class TestLoginRout(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['SERVER_NAME'] = 'localhost:5000'
        with app.app_context():
            database.create_all()

    def test_login_rout(self):
        with app.app_context():
            user = Usuario(usuario='sandoval60', email='sandoval60@gmail.com', senha=bcrypt.generate_password_hash('123456').decode('utf-8'))
            database.session.add(user)
            database.session.commit()

            response = self.app.post(url_for('login'), data=dict(
                usuario='sandoval60',
                senha='123456'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()