from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Venda(Base):
    __tablename__ = "venda"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    funcionario_id: Mapped[int] = mapped_column(ForeignKey("funcionario.id"), nullable=False)

    cliente: Mapped[Cliente] = relationship(back_populates="vendas")
    funcionario: Mapped[Funcionario] = relationship(back_populates="vendas")
    itens: Mapped[list[ItemVenda]] = relationship(back_populates="venda")
