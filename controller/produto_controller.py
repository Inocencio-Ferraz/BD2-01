from model.produto import produto
from dao.produto_dao import produtoDAO


class produtoController:

    def __init__(self, session):
        self.dao = produtoDAO(session)

    def cadastrar_cliente(self, nome, preco, quantidade_estoque, categoria):

        produto = produto(
            nome=nome,
            preco = preco,
            quantidade_estoque = quantidade_estoque,
            categoria = categoria
        )

        self.dao.cadastrar(produto)

        print("Produto cadastrado com sucesso!")