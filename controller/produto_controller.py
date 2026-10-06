from decimal import Decimal

from dto.produto_dto import ProdutoDTO
from service.produto_service import ProdutoService


class ProdutoController:
    def __init__(self, session) -> None:
        self.service = ProdutoService(session)

    def cadastrar_produto(
        self,
        nome: str,
        preco: Decimal | int | str,
        quantidade_estoque: int,
        categoria: str,
    ) -> ProdutoDTO:
        entidade = self.service.cadastrar(nome, preco, quantidade_estoque, categoria)
        return ProdutoDTO.de_entidade(entidade)

    def listar_produtos(self) -> list[ProdutoDTO]:
        return [ProdutoDTO.de_entidade(produto) for produto in self.service.listar()]

    def buscar_produto_por_id(self, produto_id: int) -> ProdutoDTO | None:
        produto = self.service.buscar_por_id(produto_id)
        return ProdutoDTO.de_entidade(produto) if produto is not None else None

    def atualizar_produto(self, produto_id: int, dados: dict) -> ProdutoDTO | None:
        produto = self.service.atualizar(produto_id, dados)
        return ProdutoDTO.de_entidade(produto) if produto is not None else None

    def remover_produto(self, produto_id: int) -> bool:
        return self.service.remover(produto_id)
