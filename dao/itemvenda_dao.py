from dao.base_dao import BaseDAO
from model.itemvenda import ItemVenda


class ItemVendaDAO(BaseDAO[ItemVenda]):
    model = ItemVenda
