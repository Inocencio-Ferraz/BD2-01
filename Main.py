from decimal import Decimal, InvalidOperation

from controller.cliente_controller import ClienteController
from controller.funcionario_controller import FuncionarioController
from controller.produto_controller import ProdutoController
from controller.venda_controller import VendaController
from database.connection import Session
from dto.itemvenda_dto import ItemVendaDTO
from dto.venda_dto import VendaDTO


def ler_inteiro(mensagem: str) -> int:
    try:
        return int(input(mensagem))
    except ValueError:
        raise ValueError("Informe um número inteiro válido.") from None


def ler_decimal(mensagem: str) -> Decimal:
    try:
        return Decimal(input(mensagem).replace(",", "."))
    except (InvalidOperation, ValueError):
        raise ValueError("Informe um valor numérico válido.") from None


def executar_acao(acao) -> None:
    try:
        acao()
    except Exception as erro:
        print(f"Erro: {erro}")


def exibir_cliente(cliente) -> None:
    print(f"ID: {cliente.id} | Nome: {cliente.nome} | CPF: {cliente.cpf} | Telefone: {cliente.telefone}")


def exibir_funcionario(funcionario) -> None:
    print(
        f"ID: {funcionario.id} | Nome: {funcionario.nome} | "
        f"CPF: {funcionario.cpf} | Função: {funcionario.funcao}"
    )


def exibir_produto(produto) -> None:
    print(
        f"ID: {produto.id} | {produto.nome} | R$ {produto.preco:.2f} | "
        f"Estoque: {produto.quantidade_estoque} | Categoria: {produto.categoria}"
    )


def exibir_venda(venda) -> None:
    data = venda.data_hora.strftime("%d/%m/%Y %H:%M") if venda.data_hora else "não informada"
    print(
        f"Venda {venda.id} | Data: {data} | Cliente: {venda.cliente_id} | "
        f"Funcionário: {venda.funcionario_id}"
    )
    for item in venda.itens:
        print(
            f"  Produto {item.produto_id} | Quantidade: {item.quantidade} | "
            f"Unitário: R$ {item.preco_unitario:.2f} | "
            f"Subtotal: R$ {item.preco_unitario * item.quantidade:.2f}"
        )
    print(f"Total: R$ {venda.valor_total:.2f}")


def menu_clientes(controller: ClienteController) -> None:
    while True:
        print("\n--- CLIENTES ---")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Buscar cliente por ID")
        print("4 - Atualizar cliente")
        print("5 - Remover cliente")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            return
        if opcao == "1":
            def cadastrar() -> None:
                dto = controller.cadastrar_cliente(
                    input("Nome: ").strip(),
                    input("CPF: ").strip(),
                    input("Telefone: ").strip(),
                )
                print("Cliente cadastrado:")
                exibir_cliente(dto)

            executar_acao(cadastrar)
        elif opcao == "2":
            def listar() -> None:
                clientes = controller.listar_clientes()
                if not clientes:
                    print("Nenhum cliente cadastrado.")
                for cliente in clientes:
                    exibir_cliente(cliente)

            executar_acao(listar)
        elif opcao == "3":
            def buscar() -> None:
                cliente = controller.buscar_cliente_por_id(ler_inteiro("ID do cliente: "))
                print("Cliente não encontrado.") if cliente is None else exibir_cliente(cliente)

            executar_acao(buscar)
        elif opcao == "4":
            def atualizar() -> None:
                cliente_id = ler_inteiro("ID do cliente: ")
                atual = controller.buscar_cliente_por_id(cliente_id)
                if atual is None:
                    print("Cliente não encontrado.")
                    return
                print("Deixe em branco para manter o valor atual.")
                dados = {}
                for campo in ("nome", "cpf", "telefone"):
                    valor = input(f"{campo.capitalize()} [{getattr(atual, campo)}]: ").strip()
                    if valor:
                        dados[campo] = valor
                if not dados:
                    print("Nenhuma alteração informada.")
                    return
                atualizado = controller.atualizar_cliente(cliente_id, dados)
                print("Cliente atualizado:")
                exibir_cliente(atualizado)

            executar_acao(atualizar)
        elif opcao == "5":
            def remover() -> None:
                cliente_id = ler_inteiro("ID do cliente: ")
                if input("Confirmar remoção? (s/n): ").strip().lower() == "s":
                    print("Cliente removido." if controller.remover_cliente(cliente_id) else "Cliente não encontrado.")

            executar_acao(remover)
        else:
            print("Opção inválida.")


def menu_funcionarios(controller: FuncionarioController) -> None:
    while True:
        print("\n--- FUNCIONÁRIOS ---")
        print("1 - Cadastrar funcionário")
        print("2 - Listar funcionários")
        print("3 - Buscar funcionário por ID")
        print("4 - Atualizar funcionário")
        print("5 - Remover funcionário")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            return
        if opcao == "1":
            def cadastrar() -> None:
                funcionario = controller.cadastrar_funcionario(
                    input("Nome: ").strip(),
                    input("CPF: ").strip(),
                    input("Função: ").strip(),
                )
                print("Funcionário cadastrado:")
                exibir_funcionario(funcionario)

            executar_acao(cadastrar)
        elif opcao == "2":
            def listar() -> None:
                funcionarios = controller.listar_funcionarios()
                if not funcionarios:
                    print("Nenhum funcionário cadastrado.")
                for funcionario in funcionarios:
                    exibir_funcionario(funcionario)

            executar_acao(listar)
        elif opcao == "3":
            def buscar() -> None:
                funcionario = controller.buscar_funcionario_por_id(ler_inteiro("ID do funcionário: "))
                print("Funcionário não encontrado.") if funcionario is None else exibir_funcionario(funcionario)

            executar_acao(buscar)
        elif opcao == "4":
            def atualizar() -> None:
                funcionario_id = ler_inteiro("ID do funcionário: ")
                atual = controller.buscar_funcionario_por_id(funcionario_id)
                if atual is None:
                    print("Funcionário não encontrado.")
                    return
                print("Deixe em branco para manter o valor atual.")
                dados = {}
                for campo in ("nome", "cpf", "funcao"):
                    valor = input(f"{campo.capitalize()} [{getattr(atual, campo)}]: ").strip()
                    if valor:
                        dados[campo] = valor
                if not dados:
                    print("Nenhuma alteração informada.")
                    return
                atualizado = controller.atualizar_funcionario(funcionario_id, dados)
                print("Funcionário atualizado:")
                exibir_funcionario(atualizado)

            executar_acao(atualizar)
        elif opcao == "5":
            def remover() -> None:
                funcionario_id = ler_inteiro("ID do funcionário: ")
                if input("Confirmar remoção? (s/n): ").strip().lower() == "s":
                    removido = controller.remover_funcionario(funcionario_id)
                    print("Funcionário removido." if removido else "Funcionário não encontrado.")

            executar_acao(remover)
        else:
            print("Opção inválida.")


def menu_produtos(controller: ProdutoController) -> None:
    while True:
        print("\n--- PRODUTOS ---")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Buscar produto por ID")
        print("4 - Atualizar produto")
        print("5 - Remover produto")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            return
        if opcao == "1":
            def cadastrar() -> None:
                produto = controller.cadastrar_produto(
                    input("Nome: ").strip(),
                    ler_decimal("Preço: R$ "),
                    ler_inteiro("Quantidade em estoque: "),
                    input("Categoria: ").strip(),
                )
                print("Produto cadastrado:")
                exibir_produto(produto)

            executar_acao(cadastrar)
        elif opcao == "2":
            def listar() -> None:
                produtos = controller.listar_produtos()
                if not produtos:
                    print("Nenhum produto cadastrado.")
                for produto in produtos:
                    exibir_produto(produto)

            executar_acao(listar)
        elif opcao == "3":
            def buscar() -> None:
                produto = controller.buscar_produto_por_id(ler_inteiro("ID do produto: "))
                print("Produto não encontrado.") if produto is None else exibir_produto(produto)

            executar_acao(buscar)
        elif opcao == "4":
            def atualizar() -> None:
                produto_id = ler_inteiro("ID do produto: ")
                atual = controller.buscar_produto_por_id(produto_id)
                if atual is None:
                    print("Produto não encontrado.")
                    return
                print("Deixe em branco para manter o valor atual.")
                dados = {}
                nome = input(f"Nome [{atual.nome}]: ").strip()
                if nome:
                    dados["nome"] = nome
                preco = input(f"Preço [{atual.preco:.2f}]: ").strip()
                if preco:
                    try:
                        dados["preco"] = Decimal(preco.replace(",", "."))
                    except InvalidOperation:
                        raise ValueError("Informe um preço numérico válido.") from None
                estoque = input(f"Estoque [{atual.quantidade_estoque}]: ").strip()
                if estoque:
                    try:
                        dados["quantidade_estoque"] = int(estoque)
                    except ValueError:
                        raise ValueError("Informe o estoque como número inteiro.") from None
                categoria = input(f"Categoria [{atual.categoria}]: ").strip()
                if categoria:
                    dados["categoria"] = categoria
                if not dados:
                    print("Nenhuma alteração informada.")
                    return
                atualizado = controller.atualizar_produto(produto_id, dados)
                print("Produto atualizado:")
                exibir_produto(atualizado)

            executar_acao(atualizar)
        elif opcao == "5":
            def remover() -> None:
                produto_id = ler_inteiro("ID do produto: ")
                if input("Confirmar remoção? (s/n): ").strip().lower() == "s":
                    removido = controller.remover_produto(produto_id)
                    print("Produto removido." if removido else "Produto não encontrado.")

            executar_acao(remover)
        else:
            print("Opção inválida.")


def menu_vendas(controller: VendaController) -> None:
    while True:
        print("\n--- VENDAS ---")
        print("1 - Criar venda")
        print("2 - Consultar venda por ID")
        print("3 - Listar vendas")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            return
        if opcao == "1":
            def criar() -> None:
                cliente_id = ler_inteiro("ID do cliente: ")
                funcionario_id = ler_inteiro("ID do funcionário: ")
                itens = []
                while True:
                    produto_id = ler_inteiro("ID do produto: ")
                    quantidade = ler_inteiro("Quantidade: ")
                    itens.append(
                        ItemVendaDTO(
                            venda_id=0,
                            produto_id=produto_id,
                            quantidade=quantidade,
                            preco_unitario=Decimal("0.00"),
                        )
                    )
                    if input("Adicionar outro produto? (s/n): ").strip().lower() != "s":
                        break
                venda = controller.criar_venda(
                    VendaDTO(cliente_id=cliente_id, funcionario_id=funcionario_id, itens=itens)
                )
                print("Venda concluída:")
                exibir_venda(venda)

            executar_acao(criar)
        elif opcao == "2":
            def buscar() -> None:
                venda = controller.buscar_venda_por_id(ler_inteiro("ID da venda: "))
                print("Venda não encontrada.") if venda is None else exibir_venda(venda)

            executar_acao(buscar)
        elif opcao == "3":
            def listar() -> None:
                vendas = controller.listar_vendas()
                if not vendas:
                    print("Nenhuma venda cadastrada.")
                for venda in vendas:
                    exibir_venda(venda)

            executar_acao(listar)
        else:
            print("Opção inválida.")


def executar_menu() -> None:
    with Session() as session:
        clientes = ClienteController(session)
        funcionarios = FuncionarioController(session)
        produtos = ProdutoController(session)
        vendas = VendaController(session)

        while True:
            print("\n================================")
            print("             PADARIA")
            print("================================")
            print("1 - Clientes")
            print("2 - Funcionários")
            print("3 - Produtos")
            print("4 - Vendas")
            print("0 - Sair")
            try:
                opcao = input("Escolha uma opção: ").strip()
            except EOFError:
                print("\nEncerrando a aplicação.")
                return

            if opcao == "0":
                print("Até logo!")
                return
            if opcao == "1":
                menu_clientes(clientes)
            elif opcao == "2":
                menu_funcionarios(funcionarios)
            elif opcao == "3":
                menu_produtos(produtos)
            elif opcao == "4":
                menu_vendas(vendas)
            else:
                print("Opção inválida.")


def main() -> None:
    try:
        executar_menu()
    except KeyboardInterrupt:
        print("\nAplicação encerrada pelo usuário.")
    except Exception as erro:
        print(f"Não foi possível iniciar a aplicação: {erro}")


if __name__ == "__main__":
    main()
