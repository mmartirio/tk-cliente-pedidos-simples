import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox, ttk
from models import Cliente


class ClienteForm(Toplevel):
    def __init__(self, master=None, cliente=None, on_save=None):
        super().__init__(master)
        self.cliente = cliente
        self.on_save = on_save
        self.title("Formulário de Cliente")
        self.geometry("350x220")
        self.resizable(False, False)

        # Frame do formulário
        frame_form = tk.Frame(self)
        frame_form.pack(padx=15, pady=10, fill='both', expand=True)

        tk.Label(frame_form, text="Nome:").pack(anchor='w')
        self.entry_nome = tk.Entry(frame_form, width=40)
        self.entry_nome.pack(pady=(0, 5))

        tk.Label(frame_form, text="Email:").pack(anchor='w')
        self.entry_email = tk.Entry(frame_form, width=40)
        self.entry_email.pack(pady=(0, 5))

        tk.Label(frame_form, text="Telefone:").pack(anchor='w')
        self.entry_telefone = tk.Entry(frame_form, width=40)
        self.entry_telefone.pack(pady=(0, 5))

        # Inserir dados se for edição
        if self.cliente:
            self.entry_nome.insert(0, self.cliente[1])
            self.entry_email.insert(0, self.cliente[2])
            self.entry_telefone.insert(0, self.cliente[3])

        # Frame dos botões
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)

        btn_salvar = tk.Button(frame_botoes, text="Salvar", command=self.salvar)
        btn_salvar.pack(side='left', padx=5)

        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side='left', padx=5)

    def validar(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório.")
            return None
        if email and "@" not in email:
            messagebox.showerror("Erro", "O campo Email é inválido.")
            return None
        if not telefone:
            messagebox.showerror("Erro", "O campo Telefone é obrigatório.")
            return None
        return nome, email, telefone

    def salvar(self):
        dados = self.validar()
        if not dados:
            return

        nome, email, telefone = dados

        if self.cliente:
            sucesso = Cliente.atualizar(self.cliente[0], nome, email, telefone)
        else:
            sucesso = Cliente.criar(nome, email, telefone)

        if sucesso:
            messagebox.showinfo("Sucesso", "Cliente salvo com sucesso.")
            if self.on_save:
                self.on_save()
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao salvar o cliente.")


class ClientesView(tk.Frame):
        """Listagem de clientes"""
        def __init__(self, master=None):
            super().__init__(master)
            self.master = master
            self.pagina_atual = 1
            self.itens_por_pagina = 10
            self.total_paginas = 1
            self.pack()
            self.create_widgets()
            self.carregar_clientes()
    
        def create_widgets(self):
            #Barra de busca
            frame_busca = tk.Frame(self)
            frame_busca.pack(fill="x", pady=5, padx=5)
            tk.Label(frame_busca, text="Buscar:").pack(side=tk.LEFT)
            self.entry_busca = tk.Entry(frame_busca, width=30)
            self.entry_busca.pack(side=tk.LEFT, padx=5)
            tk.Button(frame_busca, text="Pesquisar", command=lambda: self.carregar_clientes(resetar_pagina=True)).pack(side=tk.LEFT)

            frame_botoes = tk.Frame(self)
            frame_botoes.pack(fill="x", pady=5, padx=5)

            tk.Button(frame_botoes, text="Novo", command=self.novo_cliente).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_botoes, text="Editar", command=self.editar_cliente).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_botoes, text="Excluir", command=self.deletar_cliente).pack(side=tk.LEFT, padx=5)

            #Treeview de clientes
            self.tree = ttk.Treeview(self, columns=("id", "Nome", "Email", "Telefone"), show="headings", height=10)
            self.tree.pack(fill="both", expand=True, padx=5, pady=5)

            for col, text in zip(("id", "Nome", "Email", "Telefone"), ("ID", "Nome", "Email", "Telefone")):
                self.tree.heading(col, text=text)
                if col == "id":
                    self.tree.column(col, width=80)
                elif col == "Nome":
                    self.tree.column(col, width=200)
                elif col == "Email":
                    self.tree.column(col, width=200)
                else:
                    self.tree.column(col, width=150)

            # Controles de paginação
            frame_paginacao = tk.Frame(self)
            frame_paginacao.pack(fill="x", pady=5, padx=5)

            self.btn_primeira = tk.Button(frame_paginacao, text="<<", command=self.primeira_pagina, width=5)
            self.btn_primeira.pack(side=tk.LEFT, padx=2)

            self.btn_anterior = tk.Button(frame_paginacao, text="<", command=self.pagina_anterior, width=5)
            self.btn_anterior.pack(side=tk.LEFT, padx=2)

            self.label_pagina = tk.Label(frame_paginacao, text="Página 1 de 1")
            self.label_pagina.pack(side=tk.LEFT, padx=10)

            self.btn_proxima = tk.Button(frame_paginacao, text=">", command=self.proxima_pagina, width=5)
            self.btn_proxima.pack(side=tk.LEFT, padx=2)

            self.btn_ultima = tk.Button(frame_paginacao, text=">>", command=self.ultima_pagina, width=5)
            self.btn_ultima.pack(side=tk.LEFT, padx=2)

            self.label_total = tk.Label(frame_paginacao, text="Total: 0 registros")
            self.label_total.pack(side=tk.RIGHT, padx=10)

        def carregar_clientes(self, resetar_pagina=False):
            """Carrega os clientes na Treeview com paginação"""
            if resetar_pagina:
                self.pagina_atual = 1

            filtro = self.entry_busca.get().strip()
            todos_clientes = Cliente.listar(filtro)
            total_registros = len(todos_clientes)

            # Calcula total de páginas
            self.total_paginas = max(1, (total_registros + self.itens_por_pagina - 1) // self.itens_por_pagina)

            # Ajusta página atual se necessário
            if self.pagina_atual > self.total_paginas:
                self.pagina_atual = self.total_paginas

            # Calcula índices para paginação
            inicio = (self.pagina_atual - 1) * self.itens_por_pagina
            fim = inicio + self.itens_por_pagina
            clientes_pagina = todos_clientes[inicio:fim]

            # Limpa e insere dados
            for i in self.tree.get_children():
                self.tree.delete(i)

            for cliente in clientes_pagina:
                self.tree.insert("", "end", values=cliente)

            # Atualiza controles de paginação
            self.atualizar_controles_paginacao(total_registros)

        def novo_cliente(self):
            """Abre o formulário para criar um novo cliente"""
            def on_save():
                self.carregar_clientes()
            ClienteForm(self.master, on_save=on_save)
        
        def editar_cliente(self):
            """Abre o formulário para editar o cliente selecionado"""
            selecionado = self.tree.selection()
            if not selecionado:
                messagebox.showinfo("Editar Cliente", "Selecione um cliente para editar.")
                return
            dados = self.tree.item(selecionado[0])['values']
            ClienteForm(self.master, cliente=dados, on_save=self.carregar_clientes)

        def deletar_cliente(self):
            """Deleta o cliente selecionado"""
            selecionado = self.tree.selection()
            if not selecionado:
                messagebox.showinfo("Deletar Cliente", "Selecione um cliente para deletar.")
                return
            dados = self.tree.item(selecionado[0])['values']
            confirmar = messagebox.askyesno("Deletar Cliente", f"Tem certeza que deseja deletar o cliente {dados[1]}?")
            if confirmar:
                sucesso = Cliente.deletar(dados[0])
                if sucesso:
                    messagebox.showinfo("Sucesso", "Cliente deletado com sucesso.")
                    self.carregar_clientes()
                else:
                    messagebox.showerror("Erro", "Falha ao deletar o cliente.")

        def atualizar_controles_paginacao(self, total_registros):
            """Atualiza os controles de paginação"""
            self.label_pagina.config(text=f"Página {self.pagina_atual} de {self.total_paginas}")
            self.label_total.config(text=f"Total: {total_registros} registros")

            # Habilita/desabilita botões
            self.btn_primeira.config(state=tk.NORMAL if self.pagina_atual > 1 else tk.DISABLED)
            self.btn_anterior.config(state=tk.NORMAL if self.pagina_atual > 1 else tk.DISABLED)
            self.btn_proxima.config(state=tk.NORMAL if self.pagina_atual < self.total_paginas else tk.DISABLED)
            self.btn_ultima.config(state=tk.NORMAL if self.pagina_atual < self.total_paginas else tk.DISABLED)

        def primeira_pagina(self):
            """Vai para a primeira página"""
            self.pagina_atual = 1
            self.carregar_clientes()

        def pagina_anterior(self):
            """Vai para a página anterior"""
            if self.pagina_atual > 1:
                self.pagina_atual -= 1
                self.carregar_clientes()

        def proxima_pagina(self):
            """Vai para a próxima página"""
            if self.pagina_atual < self.total_paginas:
                self.pagina_atual += 1
                self.carregar_clientes()

        def ultima_pagina(self):
            """Vai para a última página"""
            self.pagina_atual = self.total_paginas
            self.carregar_clientes()