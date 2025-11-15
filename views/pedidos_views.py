import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from models import Cliente, Pedido, ItemPedido
from db import conectar


class PedidoForm(tk.Toplevel):
    """Janela para criar um novo pedido com itens."""

    def __init__(self, master=None, on_save=None):
        super().__init__(master)
        self.title("Novo Pedido")
        self.geometry("550x500")
        self.resizable(False, False)
        self.on_save = on_save
        self.itens = []

        # Cabeçalho do pedido
        tk.Label(self, text="Cliente:").pack(pady=(10, 0), anchor="w", padx=15)
        self.clientes = Cliente.listar()
        self.combo_cliente = ttk.Combobox(
            self,
            values=[c[1] for c in self.clientes],
            state="readonly",
            width=40
        )
        self.combo_cliente.pack(padx=15)

        tk.Label(self, text="Data:").pack(pady=(10), anchor="w", padx=15)
        self.entry_data = tk.Entry(self, width=15)
        self.entry_data.insert(0, str(date.today()))
        self.entry_data.pack(padx=10)

        # Itens do pedido
        tk.Label(self, text="Itens do Pedido:").pack(pady=(15, 0), anchor="w", padx=15)
        frame_itens = tk.Frame(self)
        frame_itens.pack(fill="x", padx=15)

        tk.Label(frame_itens, text="Produto").grid(row=0, column=0, padx=5)
        tk.Label(frame_itens, text="Qtd").grid(row=0, column=1, padx=5)
        tk.Label(frame_itens, text="Preço Unit").grid(row=0, column=2, padx=5)

        self.entry_produto = tk.Entry(frame_itens, width=20)
        self.entry_qtd = tk.Entry(frame_itens, width=5)
        self.entry_preco = tk.Entry(frame_itens, width=10)

        self.entry_produto.grid(row=1, column=0, padx=5)
        self.entry_qtd.grid(row=1, column=1, padx=5)
        self.entry_preco.grid(row=1, column=2, padx=5)

        tk.Button(frame_itens, text="Adicionar", command=self.adicionar_item).grid(row=1, column=3, padx=5)
        tk.Button(frame_itens, text="Remover", command=self.remover_item).grid(row=1, column=4, padx=5)

        # Tabela de itens
        self.tree_itens = ttk.Treeview(
            self,
            columns=("produto", "quantidade", "preco_unit", "subtotal"),
            show="headings",
            height=8
        )
        self.tree_itens.pack(fill="x", padx=15, pady=10)

        for col, texto in zip(("produto", "quantidade", "preco_unit", "subtotal"),
                            ("Produto", "Qtd", "Preço Unit", "Subtotal")):
            self.tree_itens.heading(col, text=texto)
            self.tree_itens.column(col, width=100)

        # Total
        frame_total = tk.Frame(self)
        frame_total.pack(anchor="e", padx=20)
        tk.Label(frame_total, text="Total:").pack(side=tk.LEFT)
        self.label_total = tk.Label(frame_total, text="0.00", font=("Arial", 10, "bold"))
        self.label_total.pack(side=tk.LEFT, padx=5)

        # Botões
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=15)
        tk.Button(frame_botoes, text="Salvar Pedido", command=self.salvar_pedido).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def adicionar_item(self):
        produto = self.entry_produto.get().strip()
        qtd = self.entry_qtd.get().strip()
        preco = self.entry_preco.get().strip()

        if not produto or not qtd or not preco:
            messagebox.showwarning("Validação", "Preencha todos os campos do item.")
            return

        try:
            qtd = int(qtd)
            preco = float(preco)
        except ValueError:
            messagebox.showwarning("Validação", "Quantidade e preço devem ser numéricos.")
            return

        subtotal = qtd * preco
        self.itens.append((produto, qtd, preco))
        self.tree_itens.insert("", tk.END, values=(produto, qtd, preco, subtotal))
        self.atualizar_total()

        self.entry_produto.delete(0, tk.END)
        self.entry_qtd.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)

    def remover_item(self):
        selecionado = self.tree_itens.selection()
        if not selecionado:
            messagebox.showinfo("Remover", "Selecione um item para remover.")
            return
        index = self.tree_itens.index(selecionado[0])
        del self.itens[index]
        self.tree_itens.delete(selecionado[0])
        self.atualizar_total()

    def atualizar_total(self):
        total = sum(q * p for _, q, p in self.itens)
        self.label_total.config(text=f"{total:.2f}")

    def salvar_pedido(self):
        if not self.combo_cliente.get():
            messagebox.showwarning("Validação", "Selecione um cliente.")
            return
        if not self.itens:
            messagebox.showwarning("Validação", "Adicione ao menos um item.")
            return

        cliente_nome = self.combo_cliente.get()
        cliente_id = next(c[0] for c in self.clientes if c[1] == cliente_nome)
        data_pedido = self.entry_data.get()
        total = float(self.label_total.cget("text"))

        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pedidos (cliente_id, data, total) VALUES (?, ?, ?)",
                        (cliente_id, data_pedido, total))
            pedido_id = cursor.lastrowid

            for produto, qtd, preco in self.itens:
                cursor.execute(
                    "INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unit) VALUES (?, ?, ?, ?)",
                    (pedido_id, produto, qtd, preco)
                )

            conn.commit()
            messagebox.showinfo("Sucesso", "Pedido salvo com sucesso!")
            if self.on_save:
                self.on_save()
            self.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro ao salvar pedido: {e}")
        finally:
            conn.close()


class PedidosView(tk.Frame):
    """Listagem de pedidos existentes."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pagina_atual = 1
        self.itens_por_pagina = 10
        self.total_paginas = 1
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.carregar_pedidos()

    def create_widgets(self):
        frame_top = tk.Frame(self)
        frame_top.pack(fill="x", padx=5, pady=5)

        # Frame da direita (editar/excluir)
        frame_botoes = tk.Frame(frame_top)
        frame_botoes.pack(side=tk.RIGHT)

        # Botões
        tk.Button(frame_botoes, text="Novo Pedido", command=self.novo_pedido).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Editar Pedido", command=self.editar_pedido).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Excluir Pedido", command=self.excluir_pedido).pack(side=tk.LEFT, padx=5)

        # Tabela de pedidos
        self.tree = ttk.Treeview(
            self,
            columns=("id", "cliente", "data", "total"),
            show="headings",
            height=10
        )
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        for col, texto in zip(("id", "cliente", "data", "total"),
                                ("ID", "Cliente", "Data", "Total (R$)")):
            self.tree.heading(col, text=texto)
            if col == "id":
                self.tree.column(col, width=80)
            elif col == "cliente":
                self.tree.column(col, width=200)
            elif col == "data":
                self.tree.column(col, width=150)
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

    def carregar_pedidos(self):
        """Carrega todos os pedidos do banco com paginação."""
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, c.nome, p.data, p.total
                FROM pedidos p
                JOIN clientes c ON p.cliente_id = c.id
                ORDER BY p.id DESC
            """)
            todos_pedidos = cursor.fetchall()
            total_registros = len(todos_pedidos)

            # Calcula total de páginas
            self.total_paginas = max(1, (total_registros + self.itens_por_pagina - 1) // self.itens_por_pagina)

            # Ajusta página atual se necessário
            if self.pagina_atual > self.total_paginas:
                self.pagina_atual = self.total_paginas

            # Calcula índices para paginação
            inicio = (self.pagina_atual - 1) * self.itens_por_pagina
            fim = inicio + self.itens_por_pagina
            pedidos_pagina = todos_pedidos[inicio:fim]

            # Limpa e insere dados
            for i in self.tree.get_children():
                self.tree.delete(i)
            for p in pedidos_pagina:
                self.tree.insert("", tk.END, values=p)

            # Atualiza controles de paginação
            self.atualizar_controles_paginacao(total_registros)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar pedidos: {e}")
        finally:
            conn.close()

    def novo_pedido(self):
        """Abre o formulário de novo pedido."""
        PedidoForm(self.master, on_save=self.carregar_pedidos)

    def editar_pedido(self):
        """Abre o formulário de edição do pedido selecionado."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Editar", "Selecione um pedido para editar.")
            return

        pedido_id = self.tree.item(selecionado[0], "values")[0]

        # Buscar dados do pedido
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, c.id, c.nome, p.data, p.total
                FROM pedidos p
                JOIN clientes c ON p.cliente_id = c.id
                WHERE p.id = ?
            """, (pedido_id,))
            pedido = cursor.fetchone()

            if not pedido:
                messagebox.showerror("Erro", "Pedido não encontrado.")
                return

            # Buscar itens do pedido
            cursor.execute("""
                SELECT produto, quantidade, preco_unit
                FROM itens_pedido
                WHERE pedido_id = ?
            """, (pedido_id,))
            itens = cursor.fetchall()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar pedido: {e}")
            return
        finally:
            conn.close()

        # Criar formulário de edição
        form = PedidoForm(self.master, on_save=self.carregar_pedidos)
        form.title("Editar Pedido")

        # Preenche dados do pedido
        form.combo_cliente.set(pedido[2])
        form.entry_data.delete(0, tk.END)
        form.entry_data.insert(0, pedido[3])
        form.itens = []

        # Preenche itens
        for produto, qtd, preco in itens:
            subtotal = qtd * preco
            form.itens.append((produto, qtd, preco))
            form.tree_itens.insert("", tk.END, values=(produto, qtd, preco, subtotal))
        form.atualizar_total()

        # Substitui comportamento do botão "Salvar"
        def salvar_edicao():
            cliente_id = next(c[0] for c in form.clientes if c[1] == form.combo_cliente.get())
            data_pedido = form.entry_data.get()
            total = float(form.label_total.cget("text"))

            conn = conectar()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE pedidos
                    SET cliente_id=?, data=?, total=?
                    WHERE id=?
                """, (cliente_id, data_pedido, total, pedido_id))

                cursor.execute("DELETE FROM itens_pedido WHERE pedido_id=?", (pedido_id,))
                for produto, qtd, preco in form.itens:
                    cursor.execute("""
                        INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unit)
                        VALUES (?, ?, ?, ?)
                    """, (pedido_id, produto, qtd, preco))

                conn.commit()
                messagebox.showinfo("Sucesso", "Pedido atualizado com sucesso!")
                form.destroy()
                self.carregar_pedidos()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Erro", f"Erro ao atualizar pedido: {e}")
            finally:
                conn.close()

        # Sobrescreve o método padrão
        form.salvar_pedido = salvar_edicao

    def excluir_pedido(self):
        """Exclui o pedido selecionado."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Excluir", "Selecione um pedido para excluir.")
            return

        pedido_id = self.tree.item(selecionado[0], "values")[0]

        if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este pedido?"):
            return

        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM itens_pedido WHERE pedido_id=?", (pedido_id,))
            cursor.execute("DELETE FROM pedidos WHERE id=?", (pedido_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Pedido excluído com sucesso!")
            self.carregar_pedidos()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro ao excluir pedido: {e}")
        finally:
            conn.close()

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
        self.carregar_pedidos()

    def pagina_anterior(self):
        """Vai para a página anterior"""
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_pedidos()

    def proxima_pagina(self):
        """Vai para a próxima página"""
        if self.pagina_atual < self.total_paginas:
            self.pagina_atual += 1
            self.carregar_pedidos()

    def ultima_pagina(self):
        """Vai para a última página"""
        self.pagina_atual = self.total_paginas
        self.carregar_pedidos()
