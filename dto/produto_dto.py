from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(slots=True)
class ProdutoDTO:
    nome: str
    preco: Decimal
    quantidade_estoque: int
    categoria: str
    id: int | None = None

    @classmethod
    def de_entidade(cls, entidade: Any) -> "ProdutoDTO":
        return cls(
            id=entidade.id,
            nome=entidade.nome,
            preco=entidade.preco,
            quantidade_estoque=entidade.quantidade_estoque,
            categoria=entidade.categoria,
        )
