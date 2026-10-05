# BD2-01

## Descrição

Sistema de gerenciamento de uma padaria, desenvolvido para a disciplina de Banco de Dados 2. A aplicação permite manter clientes, funcionários e produtos, além de registrar vendas com seus itens, calcular o total e atualizar o estoque.

## Tecnologias

- Python
- MariaDB
- SQLAlchemy

## Modelagem

O sistema possui cinco entidades:

- **Cliente**: nome, CPF e telefone.
- **Funcionario**: nome, CPF e função.
- **Produto**: nome, preço, quantidade em estoque e categoria.
- **Venda**: data e hora, valor total, cliente e funcionário responsáveis.
- **ItemVenda**: produto, quantidade e preço unitário registrado na venda.

Um cliente pode ter várias vendas, assim como um funcionário. Cada venda possui vários itens, e cada produto pode aparecer em vários itens de venda. `ItemVenda` representa a associação entre Venda e Produto e guarda a quantidade e o preço unitário de cada produto vendido.
