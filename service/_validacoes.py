import re
from collections.abc import Iterable
from typing import Any


def texto_obrigatorio(valor: Any, campo: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} é obrigatório.")
    return valor.strip()


def normalizar_cpf(valor: Any) -> str:
    cpf = re.sub(r"\D", "", texto_obrigatorio(valor, "CPF"))
    if len(cpf) != 11:
        raise ValueError("CPF deve conter 11 dígitos.")
    return cpf


def validar_campos(dados: dict[str, Any], permitidos: Iterable[str]) -> None:
    if not isinstance(dados, dict):
        raise ValueError("Os dados de atualização devem ser informados em um dicionário.")
    invalidos = set(dados) - set(permitidos)
    if invalidos:
        raise ValueError(f"Campos não permitidos: {', '.join(sorted(invalidos))}")
