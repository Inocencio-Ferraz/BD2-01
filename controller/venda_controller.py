from dto.itemvenda_dto import ItemVendaDTO
from dto.itemvenda_entrada import ItemVendaEntrada
from dto.venda_entrada import VendaEntrada
from dto.venda_dto import VendaDTO
from service.venda_service import VendaService


class VendaController:
    def __init__(self, session) -> None:
        self.service = VendaService(session)

    def criar_venda(self, venda: VendaEntrada) -> VendaDTO:
        entidade = self.service.criar_venda(venda)
        return VendaDTO.de_entidade(entidade)

    def adicionar_item(
        self,
        venda_id: int,
        item: ItemVendaEntrada,
    ) -> ItemVendaDTO:
        entidade = self.service.adicionar_item(venda_id, item)
        return ItemVendaDTO.de_entidade(entidade)

    def adicionar_itens(
        self,
        venda_id: int,
        itens: list[ItemVendaEntrada],
    ) -> list[ItemVendaDTO]:
        entidades = self.service.adicionar_itens(venda_id, itens)
        return [ItemVendaDTO.de_entidade(item) for item in entidades]

    def buscar_venda_por_id(self, venda_id: int) -> VendaDTO | None:
        venda = self.service.buscar_por_id(venda_id)
        return VendaDTO.de_entidade(venda) if venda is not None else None

    def listar_vendas(self) -> list[VendaDTO]:
        return [VendaDTO.de_entidade(venda) for venda in self.service.listar()]
