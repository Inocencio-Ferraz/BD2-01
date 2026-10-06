from dataclasses import dataclass

from dto.itemvenda_entrada import ItemVendaEntrada


@dataclass(slots=True)
class VendaEntrada:
    cliente_id: int
    funcionario_id: int
    itens: list[ItemVendaEntrada]
