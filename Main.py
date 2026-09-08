import produtos.Salgados as Salgados
import produtos.Doces as Doces
import produtos.Outros as Outros

#Padaria
while True:
    print("Bem-vindo à Padaria!")
    print("0. Comprar Pães")
    print("1. Comprar Salgados")
    print("2. Comprar Doces")
    print("3. Outros")
    print("4. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '0':
        print("Você comprou um pão!")

    elif opcao == "1":
        print()
        print("Opções de Salgados:")
        for salgado in Salgados.listar_salgados():
            print(f"{salgado['nome']}: R$ {salgado['preco']:.2f}")
        print()
        break

    elif opcao == "2":
        print("Você comprou um bolo!")
        print("Opções de Doces:")
        print(Doces.Doces)

    elif opcao == "3":
        print("Opções de Outros:")
        print(Outros.Outros)

    elif opcao == "4":
        print("Obrigado por visitar a Padaria!")
        break

    else:
        print("Opção inválida. Por favor, tente novamente.")