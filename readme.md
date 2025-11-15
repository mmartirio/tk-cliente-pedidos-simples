# 🧠 Tkinter Clientes & Pedidos + IA

Aplicativo simples em **Python + Tkinter + SQLite** para gerenciamento de **clientes e pedidos**, com modelagem básica e uso responsável de **IA** para acelerar o desenvolvimento.

---

## 📁 Estrutura do Projeto

tk-clientes-pedidos/
├─ main.py # Interface principal do app
├─ db.py # Inicialização e acesso ao banco SQLite
├─ models.py # Modelos de dados (Cliente, Pedido, ItemPedido)
├─ utils.py # Funções auxiliares e logs
├─ views/
│ ├─ clientes_view.py # Formulário e listagem de clientes
│ └─ pedidos_view.py # Formulário de criação de pedidos
├─ app.log # Logs automáticos de execução
└─ README.md # Documentação e registro de IA

---

## ⚙️ Requisitos

- Python **3.10+**
- Nenhuma dependência externa (somente **biblioteca padrão**)

---

## ▶️ Como Executar

1. **Clone ou baixe** o projeto.
2. No terminal, entre na pasta do projeto:
   ```bash
   cd tk-clientes-pedidos

🧩 Funcionalidades
👤 Clientes


Cadastro, edição e exclusão de clientes.


Busca por nome ou e-mail.


Validações: nome obrigatório, e-mail válido e telefone entre 8 e 15 dígitos.


🧾 Pedidos


Seleção de cliente via combobox.


Data padrão = hoje.


Adição e remoção de itens (produto, quantidade, preço unitário).


Cálculo automático do total.


Salvamento transacional em pedidos e itens_pedido.


🧠 Utilitários


Logs automáticos em app.log.


Funções de validação e mensagens centralizadas (utils.py).



🧠 Registro de IA
Durante o desenvolvimento, o assistente ChatGPT (GPT-5) foi usado de forma responsável para prototipar e revisar o código.
Abaixo, os principais prompts utilizados:
Prompt 1 — Modelagem e DB

“Crie, para um app Tkinter, o esquema de SQLite com tabelas clientes (id, nome, email, telefone) e pedidos (id, cliente_id, data, total) e itens_pedido (id, pedido_id, produto, quantidade, preco_unit). Gere funções Python em db.py para inicializar o banco e executar comandos parametrizados com tratamento de erros.”

🟢 Aceito: Código do db.py e models.py.

Prompt 2 — Formulário de Cliente

“Gere um formulário Tkinter (janela Toplevel) para cadastrar/editar Clientes com campos nome, e-mail e telefone. Valide: nome obrigatório, e-mail em formato simples, telefone com 8–15 dígitos. Inclua botões Salvar/Cancelar e callbacks separados.”

🟢 Aceito: Classe ClienteForm em clientes_view.py.

Prompt 3 — Lista de Clientes com busca

“Crie um frame Tkinter com Treeview para listar clientes, com barra de busca por nome/email e botões Novo/Editar/Excluir. Ao excluir, peça confirmação. Recarregue a lista após operações.”

🟢 Aceito com ajustes: Inclusão de confirmação e reload automático da lista.

Prompt 4 — Pedido com itens

“Implemente uma janela Tkinter para criar Pedido: selecione Cliente (Combobox), campo Data (hoje por padrão), tabela de itens (produto/quantidade/preço), botões Adicionar/Remover item e cálculo automático do total. Salve em pedidos e itens_pedido de forma transacional.”

🟢 Aceito: Estrutura de pedidos_view.py.

Prompt 5 — UX e validações

“Melhore UX do app: mensagens amigáveis (messagebox), validações com feedback, prevenção de fechar janela com dados não salvos, e try/except com logs simples.”

🟢 Aceito: Centralização de mensagens e logs em utils.py.

🧾 Observações Finais


O código foi testado localmente com Python 3.11.


Todas as funcionalidades funcionam sem dependências externas.


O uso da IA se limitou à geração e explicação de trechos de código, conforme orientações da disciplina.



Autor: Marcos Santos Martirio
Disciplina: Desenvolvimento de Interfaces com Tkinter
Professor: Mariano
Data: Novembro / 2025

---

### 💡 Explicação:
- O arquivo descreve **como rodar** o app e o que cada módulo faz.  
- Contém um **registro de IA detalhado** com os prompts usados e o que foi aceito/modificado.  
- Inclui **instruções claras** de execução e pré-requisitos.  
- É formatado para **entrega acadêmica**, simples e direto.

---

Quer que eu monte agora o **arquivo `requirements.txt`** (mesmo que opcional, só para boa prática)?


