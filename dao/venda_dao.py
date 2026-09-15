from model.venda import venda


class FuncionarioDAO:

    def __init__(self, session):
        self.session = session

    def cadastrar(self, funcionario):
        self.session.add(funcionario)
        self.session.commit()

    def listar_todos(self):
        return self.session.query(venda).all()

    def buscar_por_id(self, id):
        return self.session.query(venda).filter_by(id=id).first()

    def atualizar(self, funcionario):
        self.session.commit()

    def remover(self, funcionario):
        self.session.delete(funcionario)
        self.session.commit()