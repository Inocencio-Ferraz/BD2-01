from dao.base_dao import BaseDAO
from model.produto import Produto


class ProdutoDAO(BaseDAO[Produto]):
    model = Produto
