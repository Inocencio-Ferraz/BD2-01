# BD2-01

## Descrição

Sistema de gerenciamento de uma padaria, desenvolvido para a disciplina de Banco de Dados 2. A aplicação permite manter clientes, funcionários e produtos, além de registrar vendas com seus itens, calcular o total e atualizar o estoque.

## Tecnologias

- Python 3.12
- MariaDB
- SQLAlchemy 2.x
- MariaDB Connector/Python (`mariadb`)
- python-dotenv

## Modelagem

O sistema possui cinco entidades:

- **Cliente**: nome, CPF e telefone.
- **Funcionario**: nome, CPF e função.
- **Produto**: nome, preço, quantidade em estoque e categoria.
- **Venda**: data e hora, valor total, cliente e funcionário responsáveis.
- **ItemVenda**: produto, quantidade e preço unitário registrado na venda.

Um cliente pode ter várias vendas, assim como um funcionário. Cada venda possui vários itens, e cada produto pode aparecer em vários itens de venda. `ItemVenda` representa a associação entre Venda e Produto e guarda a quantidade e o preço unitário de cada produto vendido.

## Arquitetura

O fluxo principal é:

```text
Main.py → Controller → DTO → Service → DAO → SQLAlchemy → MariaDB
```

- **Main.py** apresenta os menus, lê os dados digitados e exibe os resultados.
- **Controller** recebe as operações da interface, usa DTOs e chama os Services.
- **DTO** transporta dados entre a interface, os Controllers e os Services.
- **Service** valida dados e aplica regras, incluindo as regras de venda e estoque.
- **DAO** concentra o acesso e as operações de persistência.
- **SQLAlchemy** mapeia as entidades e envia as operações ao MariaDB.

## Estrutura do projeto

```text
BD2-01/
├── Main.py
├── controller/
│   ├── cliente_controller.py
│   ├── funcionario_controller.py
│   ├── produto_controller.py
│   └── venda_controller.py
├── dao/
│   ├── base_dao.py
│   ├── cliente_dao.py
│   ├── funcionario_dao.py
│   ├── itemvenda_dao.py
│   ├── produto_dao.py
│   └── venda_dao.py
├── database/
│   ├── __init__.py
│   ├── base.py
│   ├── connection.py
│   └── init_db.py
├── dto/
│   ├── cliente_dto.py
│   ├── funcionario_dto.py
│   ├── itemvenda_dto.py
│   ├── produto_dto.py
│   └── venda_dto.py
├── model/
│   ├── __init__.py
│   ├── cliente.py
│   ├── funcionario.py
│   ├── itemvenda.py
│   ├── produto.py
│   └── venda.py
├── service/
│   ├── _validacoes.py
│   ├── cliente_service.py
│   ├── funcionario_service.py
│   ├── itemvenda_service.py
│   ├── produto_service.py
│   └── venda_service.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## Configuração do banco

O projeto utiliza o MariaDB e espera encontrar o banco `padaria`. A conexão é configurada por variáveis de ambiente carregadas do arquivo `.env` na raiz do projeto.

Crie seu arquivo `.env` a partir de `.env.example` e informe os dados do seu ambiente. Não compartilhe nem versione o `.env`.

Exemplo de configuração, usando apenas valores ilustrativos:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=padaria
```

O banco `padaria` precisa existir no MariaDB antes da inicialização. O comando de criação das tabelas cria ou verifica as tabelas mapeadas; não cria o banco em si.

## Instalação

Na raiz do projeto, crie e ative um ambiente virtual.

No Windows com PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Crie o `.env` a partir do exemplo. No PowerShell:

```powershell
Copy-Item .env.example .env
```

No Linux ou macOS:

```bash
cp .env.example .env
```

Edite o `.env` com as configurações locais do MariaDB.

## Criação das tabelas

Com o banco `padaria` criado e o `.env` configurado, inicialize e verifique a conexão e as tabelas com:

```bash
python -m database.init_db
```

O comando testa a conexão com uma consulta simples e executa `Base.metadata.create_all()` para criar as tabelas mapeadas que ainda não existirem.

## Execução

Com o ambiente virtual ativado, o banco disponível e as tabelas inicializadas, execute:

```bash
python Main.py
```

## Funcionalidades

- **Clientes**: cadastrar, listar, buscar por ID, atualizar e remover.
- **Funcionários**: cadastrar, listar, buscar por ID, atualizar e remover.
- **Produtos**: cadastrar, listar, buscar por ID, atualizar e remover.
- **Vendas**: criar venda, consultar por ID e listar vendas.

Uma venda pode ser criada com um ou mais produtos. O sistema registra o preço unitário aplicado, calcula o total e atualiza o estoque conforme as quantidades vendidas.

## Fluxo de venda

1. Informar o ID do cliente.
2. Informar o ID do funcionário.
3. Informar um ou mais produtos e suas quantidades.
4. Finalizar a venda.
5. O Service obtém os preços atuais dos produtos e calcula o total.
6. O estoque é atualizado e a venda é registrada.

## Observações

- Os IDs de cliente, funcionário e produto informados na venda devem corresponder a registros existentes.
- O MariaDB precisa estar em execução e acessível pelas configurações do `.env` para inicializar as tabelas e usar a aplicação.
