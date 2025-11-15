import sqlite3
from sqlite3 import Connection

DB_NAME = 'clientes_pedidos.db'

def conectar():
    """Cria uma conexão com o banco de dados SQLite."""
    try:
        conn: Connection = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
def inicializar_banco():
    """Cria as tabelas do banco de dados, se não existirem."""
    tabelas = {
        "clientes": """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT,
                telefone TEXT
            );
        """,
        "pedidos": """
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    );
""",
        "itens_pedido": """
    CREATE TABLE IF NOT EXISTS itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        produto TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unit REAL NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
    );
"""

    }

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            for name, dll in tabelas.items():
                cursor.execute(dll)
            conn.commit()
            print("Banco de dados inicializado com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar as tabelas: {e}")
        finally:
            conn.close()

def executar_comando(sql, params=()):
    """Escuta comando INSER, UPDATE, DELETE no banco de dados. Retorna True se bem-sucedido, False caso contrário."""    
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao executar comando: {e}")
            return False
        finally:
            conn.close()

def consultar(sql, params=()):
    """Escuta comando SELECT no banco de dados. Retorna os resultados ou None em caso de erro."""    
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            resultados = cursor.fetchall()
            return resultados
        except sqlite3.Error as e:
            print(f"Erro ao consultar dados: {e}")
            return None
        finally:
            conn.close()
    return None

if __name__ == "__main__":
    inicializar_banco()