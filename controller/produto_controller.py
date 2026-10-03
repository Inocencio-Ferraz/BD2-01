from dataclasses import asdict
from decimal import Decimal

from dto.produto_dto import ProdutoDTO
from service.produto_service import ProdutoService


class ProdutoController:
    def __init__(self, session) -> None:
        self.service = ProdutoService(session)

    def cadastrar_produto(
        self,
        nome: str | ProdutoDTO,
        preco: Decimal | int | str | None = None,
        quantidade_estoque: int | None = None,
        categoria: str | None = None,
    ) -> ProdutoDTO:
        dto = (
            nome
            if isinstance(nome, ProdutoDTO)
            else ProdutoDTO(nome, preco, quantidade_estoque, categoria)
        )
        entidade = self.service.cadastrar(
            dto.nome,
            dto.preco,
            dto.quantidade_estoque,
            dto.categoria,
        )
        return ProdutoDTO.de_entidade(entidade)

    def listar_produtos(self) -> list[ProdutoDTO]:
        return [ProdutoDTO.de_entidade(produto) for produto in self.service.listar()]

    def buscar_produto_por_id(self, produto_id: int) -> ProdutoDTO | None:
        produto = self.service.buscar_por_id(produto_id)
        return ProdutoDTO.de_entidade(produto) if produto is not None else None

    def atualizar_produto(self, produto_id: int, dados: dict | ProdutoDTO) -> ProdutoDTO | None:
        atualizacao = asdict(dados) if isinstance(dados, ProdutoDTO) else dict(dados)
        atualizacao.pop("id", None)
        produto = self.service.atualizar(produto_id, atualizacao)
        return ProdutoDTO.de_entidade(produto) if produto is not None else None

    def remover_produto(self, produto_id: int) -> bool:
        return self.service.remover(produto_id)
