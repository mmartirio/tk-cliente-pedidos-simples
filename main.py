import tkinter as tk
from tkinter import ttk
from db import inicializar_banco
from views.cliente_views import  ClientesView
from views.pedidos_views import PedidosView


class App(tk.Tk):
    """Aplicativo principal com menu para Clientes e Pedidos."""

    def __init__(self):
        super().__init__()
        self.title("Sistema de Clientes & Pedidos")
        self.geometry("700x500")
        self.resizable(True, True)

        # Inicializa banco de dados
        inicializar_banco()

        # Cria interface principal
        self._criar_widgets()

    def _criar_widgets(self):
        """Cria o menu e o frame principal."""
        menu_bar = tk.Menu(self)
        
        self.config(menu=menu_bar)

        # Menu Clientes
        menu_clientes = tk.Menu(menu_bar, tearoff=0)
        menu_clientes.add_command(label="Gerenciar Clientes", command=self.abrir_clientes)
        menu_bar.add_cascade(label="Clientes", menu=menu_clientes)

        # Menu Pedidos
        menu_pedidos = tk.Menu(menu_bar, tearoff=0)
        menu_pedidos.add_command(label="Gerenciar Pedidos", command=self.abrir_pedidos)
        menu_bar.add_cascade(label="Pedidos", menu=menu_pedidos)

        # Frame principal
        self.frame_principal = ttk.Frame(self)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        self.label_boas_vindas = tk.Label(
            self.frame_principal,
            text="Bem-vindo ao Sistema de Clientes e Pedidos!",
            font=("Arial", 14, "bold"),
            pady=30
        )
        self.label_boas_vindas.pack()

    def limpar_frame(self):
        """Remove widgets do frame principal antes de carregar outro."""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def abrir_clientes(self):
        """Abre a tela de listagem de clientes."""
        self.limpar_frame()
        ClientesView(master=self.frame_principal)

    def abrir_pedidos(self):
        """Abre a tela de listagem de pedidos."""
        self.limpar_frame()
        PedidosView(master=self.frame_principal)


if __name__ == "__main__":
    app = App()
    app.mainloop()
