import unittest
from site_atividade import app, database
from tests.test_cadastro_usuario import TestCadastroUsuarioRout
from tests.test_delete_usuario import TesteDeleteUsuario
from tests.test_login import TestLoginRout
from tests.test_pagamento import TestPagamentoRout
from tests.test_produtos import TestProdutosRout
from tests.test_usuario import TestUsuarioRout
from tests.test_venda import TestVendasRout


class TestIntegracao(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            database.create_all()

    def tests(self):
        test_login = TestLoginRout()
        test_login.setUp()
        test_login.test_login_rout()

        test_cadastro_usuario = TestCadastroUsuarioRout()
        test_cadastro_usuario.setUp()
        test_cadastro_usuario.test_cadastro_usuario_rout()

        test_pagamento = TestPagamentoRout()
        test_pagamento.setUp()
        test_pagamento.test_pagamento_route()

        test_produto = TestProdutosRout()
        test_produto.setUp()
        test_produto.test_produtos_rout_authenticated()
        test_produto.test_produtos_rout_unauthenticated()

        test_venda = TestVendasRout()
        test_venda.setUp()
        test_venda.test_venda_route()

        test_usuario = TestUsuarioRout()
        test_usuario.setUp()
        test_usuario.test_usuario_rout()

        test_delete_usuario = TesteDeleteUsuario()
        test_delete_usuario.setUp()
        test_delete_usuario.test_excluir_usuario()

if __name__ == '__main__':
    unittest.main()