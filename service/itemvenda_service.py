from sqlalchemy.orm import Session

from dao.itemvenda_dao import ItemVendaDAO
from model.itemvenda import ItemVenda
from service.venda_service import VendaService


class ItemVendaService:
    def __init__(self, session: Session) -> None:
        self.dao = ItemVendaDAO(session)
        self.venda_service = VendaService(session)

    def criar(self, venda_id: int, produto_id: int, quantidade: int) -> ItemVenda:
        return self.venda_service.adicionar_item(venda_id, produto_id, quantidade)

    def buscar_por_id(self, item_id: int) -> ItemVenda | None:
        return self.dao.buscar_por_id(item_id)

    def listar(self) -> list[ItemVenda]:
        return self.dao.listar()

    def atualizar(self, item_id: int, dados: dict) -> ItemVenda | None:
        if not isinstance(dados, dict) or set(dados) != {"quantidade"}:
            raise ValueError("Somente a quantidade do item pode ser atualizada.")
        return self.venda_service.atualizar_quantidade_item(item_id, dados["quantidade"])

    def remover(self, item_id: int) -> bool:
        return self.venda_service.remover_item(item_id)
