from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)

    vendas: Mapped[list[Venda]] = relationship(back_populates="cliente")
