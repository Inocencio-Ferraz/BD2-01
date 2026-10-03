from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ClienteDTO:
    nome: str
    cpf: str
    telefone: str
    id: int | None = None

    @classmethod
    def de_entidade(cls, entidade: Any) -> "ClienteDTO":
        return cls(
            id=entidade.id,
            nome=entidade.nome,
            cpf=entidade.cpf,
            telefone=entidade.telefone,
        )
