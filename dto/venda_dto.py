from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any

from dto.itemvenda_dto import ItemVendaDTO


@dataclass(slots=True)
class VendaDTO:
    cliente_id: int
    funcionario_id: int
    valor_total: Decimal = Decimal("0.00")
    itens: list[ItemVendaDTO] = field(default_factory=list)
    id: int | None = None
    data_hora: datetime | None = None

    @classmethod
    def de_entidade(cls, entidade: Any) -> "VendaDTO":
        return cls(
            id=entidade.id,
            data_hora=entidade.data_hora,
            cliente_id=entidade.cliente_id,
            funcionario_id=entidade.funcionario_id,
            valor_total=entidade.valor_total,
            itens=[ItemVendaDTO.de_entidade(item) for item in entidade.itens],
        )
