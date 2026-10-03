from collections.abc import Iterable
from decimal import Decimal

from sqlalchemy.orm import Session

from dao.cliente_dao import ClienteDAO
from dao.funcionario_dao import FuncionarioDAO
from dao.itemvenda_dao import ItemVendaDAO
from dao.produto_dao import ProdutoDAO
from dao.venda_dao import VendaDAO
from model.itemvenda import ItemVenda
from model.venda import Venda


class VendaService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.cliente_dao = ClienteDAO(session)
        self.funcionario_dao = FuncionarioDAO(session)
        self.produto_dao = ProdutoDAO(session)
        self.venda_dao = VendaDAO(session)
        self.item_dao = ItemVendaDAO(session)

    @staticmethod
    def _validar_quantidade(quantidade: int) -> int:
        if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("A quantidade do item deve ser um inteiro maior que zero.")
        return quantidade

    @classmethod
    def _normalizar_itens(cls, itens: Iterable[dict]) -> list[tuple[int, int]]:
        if isinstance(itens, (str, bytes, dict)):
            raise ValueError("Itens deve ser uma coleção de dicionários com produto_id e quantidade.")
        normalizados = []
        try:
            for item in itens:
                if not isinstance(item, dict) or "produto_id" not in item or "quantidade" not in item:
                    raise ValueError("Cada item deve informar produto_id e quantidade.")
                produto_id = item["produto_id"]
                if isinstance(produto_id, bool) or not isinstance(produto_id, int) or produto_id <= 0:
                    raise ValueError("produto_id deve ser um inteiro positivo.")
                normalizados.append((produto_id, cls._validar_quantidade(item["quantidade"])))
        except TypeError:
            raise ValueError("Itens deve ser uma coleção iterável de dicionários.") from None
        if not normalizados:
            raise ValueError("A venda deve conter pelo menos um item.")
        return normalizados

    def _adicionar_item_na_transacao(
        self,
        venda: Venda,
        produto_id: int,
        quantidade: int,
    ) -> ItemVenda:
        produto = self.produto_dao.buscar_por_id(produto_id)
        if produto is None:
            raise ValueError(f"Produto {produto_id} não existe.")
        if produto.quantidade_estoque < quantidade:
            raise ValueError(
                f"Estoque insuficiente para '{produto.nome}': "
                f"disponível {produto.quantidade_estoque}, solicitado {quantidade}."
            )

        preco_unitario = Decimal(produto.preco)
        self.produto_dao.atualizar(
            produto.id,
            {"quantidade_estoque": produto.quantidade_estoque - quantidade},
            commit=False,
        )
        item = self.item_dao.criar(
            ItemVenda(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
            ),
            commit=False,
        )
        novo_total = Decimal(venda.valor_total) + preco_unitario * quantidade
        self.venda_dao.atualizar(venda.id, {"valor_total": novo_total}, commit=False)
        return item

    def criar_venda(
        self,
        cliente_id: int,
        funcionario_id: int,
        itens: Iterable[dict],
    ) -> Venda:
        itens_normalizados = self._normalizar_itens(itens)
        try:
            cliente = self.cliente_dao.buscar_por_id(cliente_id)
            if cliente is None:
                raise ValueError(f"Cliente {cliente_id} não existe.")
            funcionario = self.funcionario_dao.buscar_por_id(funcionario_id)
            if funcionario is None:
                raise ValueError(f"Funcionário {funcionario_id} não existe.")

            venda = self.venda_dao.criar(
                Venda(
                    cliente=cliente,
                    funcionario=funcionario,
                    valor_total=Decimal("0.00"),
                ),
                commit=False,
            )
            for produto_id, quantidade in itens_normalizados:
                self._adicionar_item_na_transacao(venda, produto_id, quantidade)
            self.session.commit()
            return venda
        except Exception:
            self.session.rollback()
            raise

    def adicionar_item(self, venda_id: int, produto_id: int, quantidade: int) -> ItemVenda:
        return self.adicionar_itens(venda_id, [{"produto_id": produto_id, "quantidade": quantidade}])[0]

    def adicionar_itens(self, venda_id: int, itens: Iterable[dict]) -> list[ItemVenda]:
        itens_normalizados = self._normalizar_itens(itens)
        try:
            venda = self.venda_dao.buscar_por_id(venda_id)
            if venda is None:
                raise ValueError(f"Venda {venda_id} não existe.")
            criados = [
                self._adicionar_item_na_transacao(venda, produto_id, quantidade)
                for produto_id, quantidade in itens_normalizados
            ]
            self.session.commit()
            return criados
        except Exception:
            self.session.rollback()
            raise

    def buscar_por_id(self, venda_id: int) -> Venda | None:
        return self.venda_dao.buscar_por_id(venda_id)

    def listar(self) -> list[Venda]:
        return self.venda_dao.listar()

    def atualizar_quantidade_item(self, item_id: int, quantidade: int) -> ItemVenda | None:
        quantidade = self._validar_quantidade(quantidade)
        try:
            item = self.item_dao.buscar_por_id(item_id)
            if item is None:
                return None
            variacao = quantidade - item.quantidade
            produto = self.produto_dao.buscar_por_id(item.produto_id)
            if produto is None:
                raise ValueError(f"Produto {item.produto_id} associado ao item não existe.")
            if variacao > produto.quantidade_estoque:
                raise ValueError(
                    f"Estoque insuficiente para '{produto.nome}': "
                    f"disponível {produto.quantidade_estoque}, solicitado {variacao}."
                )
            venda = self.venda_dao.buscar_por_id(item.venda_id)
            if venda is None:
                raise ValueError(f"Venda {item.venda_id} associada ao item não existe.")

            self.produto_dao.atualizar(
                produto.id,
                {"quantidade_estoque": produto.quantidade_estoque - variacao},
                commit=False,
            )
            item_atualizado = self.item_dao.atualizar(item_id, {"quantidade": quantidade}, commit=False)
            total = Decimal(venda.valor_total) + Decimal(variacao) * Decimal(item.preco_unitario)
            self.venda_dao.atualizar(venda.id, {"valor_total": total}, commit=False)
            self.session.commit()
            return item_atualizado
        except Exception:
            self.session.rollback()
            raise

    def remover_item(self, item_id: int) -> bool:
        try:
            item = self.item_dao.buscar_por_id(item_id)
            if item is None:
                return False
            produto = self.produto_dao.buscar_por_id(item.produto_id)
            venda = self.venda_dao.buscar_por_id(item.venda_id)
            if produto is None or venda is None:
                raise ValueError("O item possui uma venda ou produto associado inexistente.")

            self.produto_dao.atualizar(
                produto.id,
                {"quantidade_estoque": produto.quantidade_estoque + item.quantidade},
                commit=False,
            )
            self.venda_dao.atualizar(
                venda.id,
                {"valor_total": Decimal(venda.valor_total) - Decimal(item.preco_unitario) * item.quantidade},
                commit=False,
            )
            self.item_dao.remover(item_id, commit=False)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise
