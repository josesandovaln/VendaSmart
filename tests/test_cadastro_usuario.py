import unittest
from flask import url_for
from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario



class TestCadastroUsuarioRout(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['SERVER_NAME'] = 'localhost:5000'
        with app.app_context():
            database.create_all()

    def test_cadastro_usuario_rout(self):
        with app.test_request_context():
            with app.app_context():
                form_data = dict(
                    usuario='sandoval80',
                    email='sandoval80@gmail.com',
                    senha='123456',
                    confirmacao='123456'
                )
                response = self.app.post(url_for('cadastro_usuario'), data=form_data, follow_redirects=True)

                self.assertEqual(response.status_code, 200)

                novo_usuario = Usuario(
                    usuario=form_data['usuario'],
                    email=form_data['email'],
                    senha=bcrypt.generate_password_hash(form_data['senha']).decode('utf-8')
                )

                database.session.add(novo_usuario)
                database.session.commit()

                usuario_cadastrado = Usuario.query.filter_by(usuario='sandoval80').first()

                self.assertIsNotNone(usuario_cadastrado)
                self.assertEqual(usuario_cadastrado.usuario, 'sandoval80')
                self.assertEqual(usuario_cadastrado.email, 'sandoval80@gmail.com')



if __name__ == '__main__':
    unittest.main()