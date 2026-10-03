from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Funcionario(Base):
    __tablename__ = "funcionario"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    funcao: Mapped[str] = mapped_column(String(80), nullable=False)

    vendas: Mapped[list[Venda]] = relationship(back_populates="funcionario")
