from site_atividade import app, database, bcrypt
from site_atividade.models import Usuario, Produtos, Categoria

#with app.app_context():
#    database.create_all()

'''Excluir o banco de dados'''
#with app.app_context():
#    database.drop_all()
#    database.create_all()

'''Inserir um registro em uma tabela usando o model da tabela'''
#with app.app_context():
#    senha_crypto = bcrypt.generate_password_hash('123456')
#    usuario = Usuario(usuario='admin', email='admin@gmail.com', senha=senha_crypto)
#   database.session.add(usuario)
#    database.session.commit()

'''Inserir um registro em uma tabela usando o model da tabela'''
#with app.app_context():
#    categoria = Categoria(categoria='Produtos de limpeza')
#    database.session.add(categoria)
#    database.session.commit()

# '''Realizar um select de todos os registros de uma tabela'''
# with app.app_context():
#     usuarios = Usuario.query.all()
#     print(usuarios[0].usuario)
#     print(usuarios[1].usuario)

'''Realizar um select de todos os registros, retornando apenas o primeiro registro'''
# with app.app_context():
#     user = Usuario.query.first()
#     print(user.usuario)

'''Realizar um select com base em um filtro e retorna os registros equivalentes à condição'''
# with app.app_context():
#    user = Usuario.query.filter_by(senha='123456').all()
#    print(user)