from model.venda import venda
from dao.venda_dao import vendaDAO


class vendaController:

    def __init__(self, session):
        self.dao = vendaDAO(session)

    def cadastrar_cliente(self, nome, valor_total, cliente_id, funcionario_id):

        venda = venda(
            nome=nome,
            cliente_id = cliente_id,
            funcionario_id = funcionario_id,
            valor_total = valor_total
        )

        self.dao.cadastrar(venda)

        print("Venda cadastrada com sucesso!")