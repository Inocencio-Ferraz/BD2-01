from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session


ModelT = TypeVar("ModelT")


class BaseDAO(Generic[ModelT]):
    """Operações CRUD comuns aos DAOs das entidades ORM."""

    model: type[ModelT]

    def __init__(self, session: Session) -> None:
        self.session = session

    def criar(self, entidade: ModelT) -> ModelT:
        try:
            self.session.add(entidade)
            self.session.commit()
            self.session.refresh(entidade)
            return entidade
        except Exception:
            self.session.rollback()
            raise

    def cadastrar(self, entidade: ModelT) -> ModelT:
        """Alias mantido para compatibilidade com os controllers existentes."""
        return self.criar(entidade)

    def listar(self) -> list[ModelT]:
        return list(self.session.scalars(select(self.model)).all())

    def listar_todos(self) -> list[ModelT]:
        """Alias mantido para compatibilidade com os DAOs anteriores."""
        return self.listar()

    def buscar_por_id(self, identificador: int) -> ModelT | None:
        return self.session.get(self.model, identificador)

    def atualizar(self, identificador: int, dados: dict[str, Any]) -> ModelT | None:
        entidade = self.buscar_por_id(identificador)
        if entidade is None:
            return None

        mapper = self.model.__mapper__
        campos_permitidos = set(mapper.column_attrs.keys()) | set(mapper.relationships.keys())
        campos_permitidos.discard("id")
        campos_invalidos = set(dados) - campos_permitidos
        if campos_invalidos:
            raise ValueError(f"Campos inválidos para {self.model.__name__}: {', '.join(sorted(campos_invalidos))}")

        try:
            for campo, valor in dados.items():
                setattr(entidade, campo, valor)
            self.session.commit()
            self.session.refresh(entidade)
            return entidade
        except Exception:
            self.session.rollback()
            raise

    def remover(self, identificador: int) -> bool:
        entidade = self.buscar_por_id(identificador)
        if entidade is None:
            return False

        try:
            self.session.delete(entidade)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise
