from sqlalchemy.orm import Session

from dao.funcionario_dao import FuncionarioDAO
from model.funcionario import Funcionario
from service._validacoes import normalizar_cpf, texto_obrigatorio, validar_campos


class FuncionarioService:
    def __init__(self, session: Session) -> None:
        self.dao = FuncionarioDAO(session)

    def _validar_cpf_disponivel(self, cpf: str, excluir_id: int | None = None) -> None:
        duplicado = any(
            funcionario.cpf == cpf and funcionario.id != excluir_id
            for funcionario in self.dao.listar()
        )
        if duplicado:
            raise ValueError("Já existe um funcionário cadastrado com este CPF.")

    def cadastrar(self, nome: str, cpf: str, funcao: str) -> Funcionario:
        nome = texto_obrigatorio(nome, "Nome")
        cpf = normalizar_cpf(cpf)
        funcao = texto_obrigatorio(funcao, "Função")
        self._validar_cpf_disponivel(cpf)
        return self.dao.criar(Funcionario(nome=nome, cpf=cpf, funcao=funcao))

    def listar(self) -> list[Funcionario]:
        return self.dao.listar()

    def buscar_por_id(self, funcionario_id: int) -> Funcionario | None:
        return self.dao.buscar_por_id(funcionario_id)

    def atualizar(self, funcionario_id: int, dados: dict) -> Funcionario | None:
        funcionario = self.dao.buscar_por_id(funcionario_id)
        if funcionario is None:
            return None
        validar_campos(dados, {"nome", "cpf", "funcao"})
        dados = dict(dados)
        if "nome" in dados:
            dados["nome"] = texto_obrigatorio(dados["nome"], "Nome")
        if "cpf" in dados:
            dados["cpf"] = normalizar_cpf(dados["cpf"])
            self._validar_cpf_disponivel(dados["cpf"], excluir_id=funcionario_id)
        if "funcao" in dados:
            dados["funcao"] = texto_obrigatorio(dados["funcao"], "Função")
        return self.dao.atualizar(funcionario_id, dados)

    def remover(self, funcionario_id: int) -> bool:
        return self.dao.remover(funcionario_id)
