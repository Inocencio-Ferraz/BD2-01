from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(slots=True)
class ItemVendaDTO:
    venda_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    id: int | None = None

    @classmethod
    def de_entidade(cls, entidade: Any) -> "ItemVendaDTO":
        return cls(
            id=entidade.id,
            venda_id=entidade.venda_id,
            produto_id=entidade.produto_id,
            quantidade=entidade.quantidade,
            preco_unitario=entidade.preco_unitario,
        )
