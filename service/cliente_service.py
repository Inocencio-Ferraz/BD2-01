from sqlalchemy.orm import Session

from dao.cliente_dao import ClienteDAO
from model.cliente import Cliente
from service._validacoes import normalizar_cpf, texto_obrigatorio, validar_campos


class ClienteService:
    def __init__(self, session: Session) -> None:
        self.dao = ClienteDAO(session)

    def _validar_cpf_disponivel(self, cpf: str, excluir_id: int | None = None) -> None:
        duplicado = any(
            cliente.cpf == cpf and cliente.id != excluir_id
            for cliente in self.dao.listar()
        )
        if duplicado:
            raise ValueError("Já existe um cliente cadastrado com este CPF.")

    def cadastrar(self, nome: str, cpf: str, telefone: str) -> Cliente:
        nome = texto_obrigatorio(nome, "Nome")
        cpf = normalizar_cpf(cpf)
        telefone = texto_obrigatorio(telefone, "Telefone")
        self._validar_cpf_disponivel(cpf)
        return self.dao.criar(Cliente(nome=nome, cpf=cpf, telefone=telefone))

    def listar(self) -> list[Cliente]:
        return self.dao.listar()

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        return self.dao.buscar_por_id(cliente_id)

    def atualizar(self, cliente_id: int, dados: dict) -> Cliente | None:
        cliente = self.dao.buscar_por_id(cliente_id)
        if cliente is None:
            return None
        validar_campos(dados, {"nome", "cpf", "telefone"})
        dados = dict(dados)
        if "nome" in dados:
            dados["nome"] = texto_obrigatorio(dados["nome"], "Nome")
        if "cpf" in dados:
            dados["cpf"] = normalizar_cpf(dados["cpf"])
            self._validar_cpf_disponivel(dados["cpf"], excluir_id=cliente_id)
        if "telefone" in dados:
            dados["telefone"] = texto_obrigatorio(dados["telefone"], "Telefone")
        return self.dao.atualizar(cliente_id, dados)

    def remover(self, cliente_id: int) -> bool:
        return self.dao.remover(cliente_id)
