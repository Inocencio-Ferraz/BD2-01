from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class FuncionarioDTO:
    nome: str
    cpf: str
    funcao: str
    id: int | None = None

    @classmethod
    def de_entidade(cls, entidade: Any) -> "FuncionarioDTO":
        return cls(
            id=entidade.id,
            nome=entidade.nome,
            cpf=entidade.cpf,
            funcao=entidade.funcao,
        )
