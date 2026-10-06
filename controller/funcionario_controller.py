from dto.funcionario_dto import FuncionarioDTO
from service.funcionario_service import FuncionarioService


class FuncionarioController:
    def __init__(self, session) -> None:
        self.service = FuncionarioService(session)

    def cadastrar_funcionario(self, nome: str, cpf: str, funcao: str) -> FuncionarioDTO:
        entidade = self.service.cadastrar(nome, cpf, funcao)
        return FuncionarioDTO.de_entidade(entidade)

    def listar_funcionarios(self) -> list[FuncionarioDTO]:
        return [FuncionarioDTO.de_entidade(item) for item in self.service.listar()]

    def buscar_funcionario_por_id(self, funcionario_id: int) -> FuncionarioDTO | None:
        funcionario = self.service.buscar_por_id(funcionario_id)
        return FuncionarioDTO.de_entidade(funcionario) if funcionario is not None else None

    def atualizar_funcionario(self, funcionario_id: int, dados: dict) -> FuncionarioDTO | None:
        funcionario = self.service.atualizar(funcionario_id, dados)
        return FuncionarioDTO.de_entidade(funcionario) if funcionario is not None else None

    def remover_funcionario(self, funcionario_id: int) -> bool:
        return self.service.remover(funcionario_id)
