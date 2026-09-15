class funcionario:
 def __init__(self, id, name, cpf, funcao):

    self.id = id
    self.name = name
    self.cpf = cpf
    self.funcao = funcao

 def mostrar_dados(self):
    print(f"ID: {self.id}")
    print(f"Nome: {self.id}")
    print(f"ID: {self.id}")
    print(f"ID: {self.id}")

 def alterar_funcao(self, nova_funcao):
        self.funcao = nova_funcao
        print(f"A função foi alterada para {nova_funcao}")

 def alterar_funcao(self, nova_funcao):
        self.funcao = nova_funcao
        print(f"A função foi alterada para {nova_funcao}")
 def registrar_entrada(self):
        self.presente = True
        print(f"{self.nome} entrou na padaria.")

 def registrar_saida(self):
        self.presente = False
        print(f"{self.nome} saiu da padaria.")    