import unittest
from flask import url_for
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario

class TestLogoutRout(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['SERVER_NAME'] = 'localhost:5000'


    def test_logout_rout(self):
        with app.app_context():
            user = Usuario(usuario='sandoval30', email='sandoval30@gmail.com',
                           senha=bcrypt.generate_password_hash('123456').decode('utf-8'))
            database.session.add(user)
            database.session.commit()

            response = self.app.post(url_for('login'), data=dict(
                usuario='sandoval30',
                senha='123456'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            response = self.app.get(url_for('logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()