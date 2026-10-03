from dataclasses import asdict

from dto.funcionario_dto import FuncionarioDTO
from service.funcionario_service import FuncionarioService


class FuncionarioController:
    def __init__(self, session) -> None:
        self.service = FuncionarioService(session)

    def cadastrar_funcionario(
        self,
        nome: str | FuncionarioDTO,
        cpf: str | None = None,
        funcao: str | None = None,
    ) -> FuncionarioDTO:
        dto = nome if isinstance(nome, FuncionarioDTO) else FuncionarioDTO(nome, cpf, funcao)
        entidade = self.service.cadastrar(dto.nome, dto.cpf, dto.funcao)
        return FuncionarioDTO.de_entidade(entidade)

    def listar_funcionarios(self) -> list[FuncionarioDTO]:
        return [FuncionarioDTO.de_entidade(item) for item in self.service.listar()]

    def buscar_funcionario_por_id(self, funcionario_id: int) -> FuncionarioDTO | None:
        funcionario = self.service.buscar_por_id(funcionario_id)
        return FuncionarioDTO.de_entidade(funcionario) if funcionario is not None else None

    def atualizar_funcionario(
        self,
        funcionario_id: int,
        dados: dict | FuncionarioDTO,
    ) -> FuncionarioDTO | None:
        atualizacao = asdict(dados) if isinstance(dados, FuncionarioDTO) else dict(dados)
        atualizacao.pop("id", None)
        funcionario = self.service.atualizar(funcionario_id, atualizacao)
        return FuncionarioDTO.de_entidade(funcionario) if funcionario is not None else None

    def remover_funcionario(self, funcionario_id: int) -> bool:
        return self.service.remover(funcionario_id)
