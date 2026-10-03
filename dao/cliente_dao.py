from dao.base_dao import BaseDAO
from model.cliente import Cliente


class ClienteDAO(BaseDAO[Cliente]):
    model = Cliente
