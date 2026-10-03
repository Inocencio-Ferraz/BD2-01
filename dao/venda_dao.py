from dao.base_dao import BaseDAO
from model.venda import Venda


class VendaDAO(BaseDAO[Venda]):
    model = Venda
