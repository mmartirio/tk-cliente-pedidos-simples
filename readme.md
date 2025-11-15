# Sistema de Gestão de Clientes e Pedidos

Sistema desktop desenvolvido em Python com Tkinter para gerenciamento de clientes e pedidos, com interface gráfica intuitiva e banco de dados SQLite.

## 📋 Funcionalidades

### Gestão de Clientes
- ✅ Cadastro completo de clientes (nome, email, telefone)
- ✅ Edição de dados cadastrais
- ✅ Exclusão de clientes
- ✅ Busca por nome, email ou telefone
- ✅ Paginação (10 registros por página)
- ✅ Validação de formulários

### Gestão de Pedidos
- ✅ Criação de pedidos com múltiplos itens
- ✅ Edição de pedidos existentes
- ✅ Exclusão de pedidos
- ✅ Visualização de todos os pedidos
- ✅ Paginação (10 registros por página)
- ✅ Cálculo automático de totais

### Itens de Pedido
- ✅ Adicionar produtos ao pedido
- ✅ Definir quantidade e preço unitário
- ✅ Remover itens do pedido
- ✅ Cálculo automático de subtotais

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter** - Interface gráfica
- **SQLite3** - Banco de dados
- **Git** - Controle de versão

## 📦 Estrutura do Projeto

```
tk-clientes-pedidos/
├── main.py                 # Arquivo principal da aplicação
├── db.py                   # Conexão e inicialização do banco
├── models.py               # Modelos Cliente, Pedido e ItemPedido
├── utils.py                # Funções auxiliares
├── views/
│   ├── __init__.py
│   ├── cliente_views.py    # Interface de clientes
│   └── pedidos_views.py    # Interface de pedidos
├── .gitignore
└── README.md
```

## 🔧 Instalação e Execução

### Pré-requisitos
- Python 3.7 ou superior instalado

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/mmartirio/tk-cliente-pedidos-simples.git
cd tk-cliente-pedidos-simples
```

2. **Execute a aplicação**
```bash
python main.py
```

O banco de dados SQLite será criado automaticamente na primeira execução.

## 💡 Como Usar

### Gerenciar Clientes
1. No menu superior, clique em **Clientes** → **Gerenciar Clientes**
2. Use os botões:
   - **Novo**: Cadastrar novo cliente
   - **Editar**: Modificar cliente selecionado
   - **Excluir**: Remover cliente selecionado
3. Use a barra de busca para filtrar clientes
4. Navegue entre páginas usando os botões `<<`, `<`, `>`, `>>`

### Gerenciar Pedidos
1. No menu superior, clique em **Pedidos** → **Gerenciar Pedidos**
2. Use os botões:
   - **Novo Pedido**: Criar novo pedido
   - **Editar Pedido**: Modificar pedido selecionado
   - **Excluir Pedido**: Remover pedido selecionado
3. Navegue entre páginas usando os controles de paginação

### Criar um Pedido
1. Clique em **Novo Pedido**
2. Selecione o cliente
3. Adicione itens:
   - Digite o nome do produto
   - Informe quantidade
   - Informe preço unitário
   - Clique em **Adicionar**
4. Clique em **Salvar Pedido**

## 🗃️ Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

### Tabela `clientes`
- `id` (INTEGER PRIMARY KEY)
- `nome` (TEXT)
- `email` (TEXT)
- `telefone` (TEXT)

### Tabela `pedidos`
- `id` (INTEGER PRIMARY KEY)
- `cliente_id` (INTEGER FOREIGN KEY)
- `data` (TEXT)
- `total` (REAL)

### Tabela `itens_pedido`
- `id` (INTEGER PRIMARY KEY)
- `pedido_id` (INTEGER FOREIGN KEY)
- `produto` (TEXT)
- `quantidade` (INTEGER)
- `preco_unit` (REAL)

## 🎨 Interface

- Interface gráfica moderna com Tkinter
- Tabelas com colunas redimensionáveis
- Paginação automática para melhor performance
- Formulários com validação de dados
- Janelas modais para edição

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional.

## 👤 Autor

**Marco Martírio**
- GitHub: [@mmartirio](https://github.com/mmartirio)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
