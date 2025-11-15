import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re


def registrar_log(mensagem):
    """Registra uma mensagem de log em arquivo local."""
    try:
        with open("app.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}\n")
    except Exception as e:
        print(f"Erro ao registrar log: {e}")


def mostrar_erro(titulo, mensagem):
    """Exibe mensagem de erro e registra log."""
    registrar_log(f"ERRO - {titulo}: {mensagem}")
    messagebox.showerror(titulo, mensagem)


def mostrar_info(titulo, mensagem):
    """Exibe mensagem informativa e registra log."""
    registrar_log(f"INFO - {titulo}: {mensagem}")
    messagebox.showinfo(titulo, mensagem)


def validar_email(email):
    """Valida formato simples de e-mail."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def validar_telefone(telefone):
    """Valida telefone com 8–15 dígitos numéricos."""
    return bool(re.match(r"^\d{8,15}$", telefone))


def confirmar_acao(titulo, mensagem):
    """Exibe caixa de confirmação e retorna True/False."""
    return messagebox.askyesno(titulo, mensagem)
