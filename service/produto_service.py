from decimal import Decimal, InvalidOperation
from typing import Any

from sqlalchemy.orm import Session

from dao.produto_dao import ProdutoDAO
from model.produto import Produto
from service._validacoes import texto_obrigatorio, validar_campos


class ProdutoService:
    def __init__(self, session: Session) -> None:
        self.dao = ProdutoDAO(session)

    @staticmethod
    def _validar_preco(valor: Any) -> Decimal:
        try:
            preco = Decimal(str(valor))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Preço deve ser um valor numérico válido.") from None
        if not preco.is_finite() or preco < 0:
            raise ValueError("Preço não pode ser negativo e deve ser finito.")
        return preco

    @staticmethod
    def _validar_estoque(valor: Any) -> int:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
            raise ValueError("Estoque deve ser um número inteiro não negativo.")
        return valor

    def cadastrar(
        self,
        nome: str,
        preco: Decimal | int | str,
        quantidade_estoque: int,
        categoria: str,
    ) -> Produto:
        produto = Produto(
            nome=texto_obrigatorio(nome, "Nome"),
            preco=self._validar_preco(preco),
            quantidade_estoque=self._validar_estoque(quantidade_estoque),
            categoria=texto_obrigatorio(categoria, "Categoria"),
        )
        return self.dao.criar(produto)

    def listar(self) -> list[Produto]:
        return self.dao.listar()

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        return self.dao.buscar_por_id(produto_id)

    def atualizar(self, produto_id: int, dados: dict) -> Produto | None:
        if self.dao.buscar_por_id(produto_id) is None:
            return None
        validar_campos(dados, {"nome", "preco", "quantidade_estoque", "categoria"})
        dados = dict(dados)
        if "nome" in dados:
            dados["nome"] = texto_obrigatorio(dados["nome"], "Nome")
        if "preco" in dados:
            dados["preco"] = self._validar_preco(dados["preco"])
        if "quantidade_estoque" in dados:
            dados["quantidade_estoque"] = self._validar_estoque(dados["quantidade_estoque"])
        if "categoria" in dados:
            dados["categoria"] = texto_obrigatorio(dados["categoria"], "Categoria")
        return self.dao.atualizar(produto_id, dados)

    def remover(self, produto_id: int) -> bool:
        return self.dao.remover(produto_id)
