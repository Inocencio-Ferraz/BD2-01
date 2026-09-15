from model.produto import produto


class FuncionarioDAO:

    def __init__(self, session):
        self.session = session

    def cadastrar(self, funcionario):
        self.session.add(funcionario)
        self.session.commit()

    def listar_todos(self):
        return self.session.query(produto).all()

    def buscar_por_id(self, id):
        return self.session.query(produto).filter_by(id=id).first()

    def atualizar(self, funcionario):
        self.session.commit()

    def remover(self, funcionario):
        self.session.delete(funcionario)
        self.session.commit()