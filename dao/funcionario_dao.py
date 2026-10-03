from dao.base_dao import BaseDAO
from model.funcionario import Funcionario


class FuncionarioDAO(BaseDAO[Funcionario]):
    model = Funcionario
