from dataclasses import dataclass


@dataclass(slots=True)
class ItemVendaEntrada:
    produto_id: int
    quantidade: int
