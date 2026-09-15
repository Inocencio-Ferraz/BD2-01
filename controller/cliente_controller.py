from model.cliente import cliente
from dao.cliente_dao import clienteDAO


class clienteController:

    def __init__(self, session):
        self.dao = clienteDAO(session)

    def cadastrar_cliente(self, nome, cpf, telefone):

        cliente = cliente(
            nome=nome,
            cpf=cpf,
            telefone = telefone
        )

        self.dao.cadastrar(cliente)

        print("Cliente cadastrado com sucesso!")