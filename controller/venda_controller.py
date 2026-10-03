from dto.itemvenda_dto import ItemVendaDTO
from dto.venda_dto import VendaDTO
from service.venda_service import VendaService


class VendaController:
    def __init__(self, session) -> None:
        self.service = VendaService(session)

    def criar_venda(self, venda: VendaDTO) -> VendaDTO:
        itens = [
            {"produto_id": item.produto_id, "quantidade": item.quantidade}
            for item in venda.itens
        ]
        entidade = self.service.criar_venda(venda.cliente_id, venda.funcionario_id, itens)
        return VendaDTO.de_entidade(entidade)

    def adicionar_item(
        self,
        venda_id: int,
        produto_id: int | ItemVendaDTO,
        quantidade: int | None = None,
    ) -> ItemVendaDTO:
        if isinstance(produto_id, ItemVendaDTO):
            quantidade = produto_id.quantidade
            produto_id = produto_id.produto_id
        entidade = self.service.adicionar_item(venda_id, produto_id, quantidade)
        return ItemVendaDTO.de_entidade(entidade)

    def adicionar_itens(self, venda_id: int, itens: list[ItemVendaDTO]) -> list[ItemVendaDTO]:
        entradas = [
            {"produto_id": item.produto_id, "quantidade": item.quantidade}
            for item in itens
        ]
        entidades = self.service.adicionar_itens(venda_id, entradas)
        return [ItemVendaDTO.de_entidade(item) for item in entidades]

    def buscar_venda_por_id(self, venda_id: int) -> VendaDTO | None:
        venda = self.service.buscar_por_id(venda_id)
        return VendaDTO.de_entidade(venda) if venda is not None else None

    def listar_vendas(self) -> list[VendaDTO]:
        return [VendaDTO.de_entidade(venda) for venda in self.service.listar()]
