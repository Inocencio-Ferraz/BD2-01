from dataclasses import asdict

from dto.cliente_dto import ClienteDTO
from service.cliente_service import ClienteService


class ClienteController:
    def __init__(self, session) -> None:
        self.service = ClienteService(session)

    def cadastrar_cliente(
        self,
        nome: str | ClienteDTO,
        cpf: str | None = None,
        telefone: str | None = None,
    ) -> ClienteDTO:
        dto = nome if isinstance(nome, ClienteDTO) else ClienteDTO(nome, cpf, telefone)
        entidade = self.service.cadastrar(dto.nome, dto.cpf, dto.telefone)
        return ClienteDTO.de_entidade(entidade)

    def listar_clientes(self) -> list[ClienteDTO]:
        return [ClienteDTO.de_entidade(cliente) for cliente in self.service.listar()]

    def buscar_cliente_por_id(self, cliente_id: int) -> ClienteDTO | None:
        cliente = self.service.buscar_por_id(cliente_id)
        return ClienteDTO.de_entidade(cliente) if cliente is not None else None

    def atualizar_cliente(self, cliente_id: int, dados: dict | ClienteDTO) -> ClienteDTO | None:
        atualizacao = asdict(dados) if isinstance(dados, ClienteDTO) else dict(dados)
        atualizacao.pop("id", None)
        cliente = self.service.atualizar(cliente_id, atualizacao)
        return ClienteDTO.de_entidade(cliente) if cliente is not None else None

    def remover_cliente(self, cliente_id: int) -> bool:
        return self.service.remover(cliente_id)
