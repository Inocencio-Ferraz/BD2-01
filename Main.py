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
        print("Opções de Salgados:")

    elif opcao == "2":
        print("Você comprou um bolo!")

    elif opcao == "3":
        print("Você comprou um refrigerante!")

    elif opcao == "4":
        print("Obrigado por visitar a Padaria!")
        break

    else:
        print("Opção inválida. Por favor, tente novamente.")