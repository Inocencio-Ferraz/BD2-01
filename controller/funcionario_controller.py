from model.funcionario import Funcionario
from dao.funcionario_dao import FuncionarioDAO


class FuncionarioController:

    def __init__(self, session):
        self.dao = FuncionarioDAO(session)

    def cadastrar_funcionario(self, nome, cpf, funcao):

        funcionario = Funcionario(
            nome=nome,
            cpf=cpf,
            funcao=funcao
        )

        self.dao.cadastrar(funcionario)

        print("Funcionário cadastrado com sucesso!")