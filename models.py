from db import executar_comando, consultar


class Cliente:
    @staticmethod
    def criar(nome, email, telefone):
        sql = "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)"
        return executar_comando(sql, (nome, email, telefone))

    @staticmethod
    def atualizar(cliente_id, nome, email, telefone):
        sql = "UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?"
        return executar_comando(sql, (nome, email, telefone, cliente_id))
    
    @staticmethod
    def listar(filtro=""):
        sql = "SELECT * FROM clientes"
        if filtro:
            sql += " WHERE nome LIKE ? OR email LIKE ? OR telefone LIKE ?"
            filtro = f"%{filtro}%"
            return consultar(sql, (filtro, filtro, filtro))
        return consultar(sql)
    
    @staticmethod
    def deletar(cliente_id):
        sql = "DELETE FROM clientes WHERE id=?"
        return executar_comando(sql, (cliente_id,))
    
class Pedido:
    """Representa um pedido e operações relacionadas no banco de dados."""

    @staticmethod
    def listar():
        """Retorna uma lista de pedidos."""
        sql = "SELECT p.id, c.nome, p.data, p.total FROM pedidos p JOIN clientes c ON p.cliente_id = c.id ORDER BY p.data DESC"
        return consultar(sql)
    
    @staticmethod
    def inserir(cliente_id, data, total):
        """Insere um novo pedido no banco de dados."""
        sql = "INSERT INTO pedidos (cliente_id, data, total) VALUES (?, ?, ?)"
        return executar_comando(sql, (cliente_id, data, total))

    @staticmethod
    def atualizar(item_id, produto, quantidade, preco_unit):
        """Atualiza os dados de um item do pedido existente."""
        sql = """
            UPDATE itens_pedido
            SET produto = ?, quantidade = ?, preco_unit = ?
            WHERE id = ?
        """
        return executar_comando(sql, (produto, quantidade, preco_unit, item_id))
    
    @staticmethod
    def excluir(pedido_id):
        """Exclui um pedido do banco de dados."""
        sql = "DELETE FROM pedidos WHERE id = ?"
        return executar_comando(sql, (pedido_id,))

    @staticmethod
    def buscar_por_id(pedido_id):
        """Retorna os dados de um pedido específico."""
        sql = """
            SELECT p.id, c.nome, p.data, p.total
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE p.id = ?
        """
        resultado = consultar(sql, (pedido_id,))
        if resultado:
            id_, cliente, data, total = resultado[0]
            return {"id": id_, "cliente": cliente, "data": data, "total": total}
        return None

class ItemPedido:
    """Representa um item de pedido e operações relacionadas no banco de dados."""

    @staticmethod
    def listar(pedido_id):
        """Retorna uma lista de itens para um pedido específico."""
        sql = "SELECT id, produto, quantidade, preco_unit FROM itens_pedido WHERE pedido_id = ?"
        return consultar(sql, (pedido_id,))

    @staticmethod
    def listar_por_pedido(pedido_id):
        """Retorna lista simples (produto, quantidade, preço) para uso em edição."""
        sql = "SELECT produto, quantidade, preco_unit FROM itens_pedido WHERE pedido_id = ?"
        return consultar(sql, (pedido_id,))

    @staticmethod
    def inserir(pedido_id, produto, quantidade, preco_unit):
        """Insere um novo item de pedido no banco de dados."""
        sql = "INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unit) VALUES (?, ?, ?, ?)"
        return executar_comando(sql, (pedido_id, produto, quantidade, preco_unit))
    
    @staticmethod
    def excluir(item_id):
        """Exclui um item de pedido do banco de dados."""
        sql = "DELETE FROM itens_pedido WHERE id = ?"
        return executar_comando(sql, (item_id,))
