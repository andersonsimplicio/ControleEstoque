# model/database.py
import sqlite3
import os


class DatabaseManager:
    def __init__(self, db_name="estoque.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(base_dir, db_name)
        self.conn = None
        self.conn = None
        self.cursor = None
        self._criar_tabelas()
        self._conectar()
        self._criar_tabelas()

    def _conectar(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Erro ao conectar à base de dados: {e}")

    def fechar(self):
        if self.conn: self.conn.close()

    def _criar_tabelas(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS pecas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT NOT NULL,
                    numero_serie TEXT,
                    marca TEXT,
                    preco_custo REAL,
                    condicao TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS entradas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    peca_id INTEGER NOT NULL,
                    FOREIGN KEY (peca_id) REFERENCES pecas(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS saidas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    peca_id INTEGER NOT NULL,
                    FOREIGN KEY (peca_id) REFERENCES pecas(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    preco_venda REAL NOT NULL,
                    canal_venda TEXT,
                    saida_id INTEGER NOT NULL,
                    FOREIGN KEY (saida_id) REFERENCES saidas(id)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro tabelas: {e}")

    # --- Métodos CRUD (Nomes alinhados com o Controller) ---

    def cadastrar_peca(self, dados):
        # Controller chama 'cadastrar_peca' (sem ç)
        self.cursor.execute("INSERT INTO pecas (descricao, numero_serie, marca, preco_custo, condicao) VALUES (?, ?, ?, ?, ?)", dados)
        self.conn.commit()

    def atualizar_peca(self, dados):
        # Controller chama 'atualizar_peca' (sem ç)
        self.cursor.execute("UPDATE pecas SET descricao=?, numero_serie=?, marca=?, preco_custo=?, condicao=? WHERE id=?", dados)
        self.conn.commit()

    def buscar_pecas(self, termo): 
        # Controller chama 'buscar_pecas'
        self.cursor.execute("SELECT id, descricao, numero_serie, marca FROM pecas WHERE descricao LIKE ? ORDER BY descricao", (f'%{termo}%',))
        return self.cursor.fetchall()

    # Alias para garantir compatibilidade caso algum código antigo chame o nome longo
    buscar_pecas_por_descricao = buscar_pecas 

    def buscar_peca_por_id(self, pid):
        self.cursor.execute("SELECT * FROM pecas WHERE id=?", (pid,))
        return self.cursor.fetchone()
    
    # Alias para 'buscar_peca_id' se necessário
    buscar_peca_id = buscar_peca_por_id

    def buscar_estoque_completo(self):
        # Controller chama 'buscar_estoque_completo'
        """Retorna todas as peças com o cálculo de estoque atual."""
        self.cursor.execute("SELECT id, descricao, numero_serie, marca, preco_custo, condicao FROM pecas ORDER BY descricao")
        pecas = self.cursor.fetchall()
        resultado = []
        for p in pecas:
            pid = p[0]
            # Calcula entradas
            self.cursor.execute("SELECT SUM(quantidade) FROM entradas WHERE peca_id=?", (pid,))
            res_ent = self.cursor.fetchone()
            ent = res_ent[0] if res_ent and res_ent[0] else 0
            
            # Calcula saídas
            self.cursor.execute("SELECT SUM(quantidade) FROM saidas WHERE peca_id=?", (pid,))
            res_sai = self.cursor.fetchone()
            sai = res_sai[0] if res_sai and res_sai[0] else 0
            
            # Adiciona saldo ao final da tupla
            resultado.append(p + (ent - sai,))
        return resultado
    
    # Alias para nome antigo, apenas por segurança
    buscar_todas_peças_com_estoque = buscar_estoque_completo

    def calcular_total_estoque(self):
        pecas = self.buscar_estoque_completo()
        # p[4] é preço custo, p[6] é a quantidade (estoque calculado acima)
        return sum((p[4] if p[4] else 0) * p[6] for p in pecas)

    def registrar_movimento(self, tabela, dados):
        if tabela not in ('entradas', 'saidas'): return
        self.cursor.execute(f"INSERT INTO {tabela} (data, quantidade, peca_id) VALUES (?, ?, ?)", dados)
        self.conn.commit()
        return self.cursor.lastrowid

    def registrar_venda(self, dados):
        self.cursor.execute("INSERT INTO vendas (data, preco_venda, canal_venda, saida_id) VALUES (?, ?, ?, ?)", dados)
        self.conn.commit()

    def buscar_historico(self, tabela, d_ini, d_fim):
        if tabela not in ('entradas', 'saidas'): return []
        # Traz o ID (m.id) para permitir exclusão
        sql = f"""
            SELECT m.id, m.data, m.quantidade, p.descricao, p.preco_custo
            FROM {tabela} m
            JOIN pecas p ON m.peca_id = p.id
            WHERE m.data BETWEEN ? AND ? ORDER BY m.data DESC
        """
        self.cursor.execute(sql, (d_ini, d_fim))
        return self.cursor.fetchall()

    def buscar_lucro(self, d_ini, d_fim):
        sql = """
            SELECT s.data, s.quantidade, p.descricao, p.preco_custo, v.preco_venda, v.canal_venda
            FROM saidas s
            JOIN pecas p ON s.peca_id = p.id
            LEFT JOIN vendas v ON s.id = v.saida_id
            WHERE s.data BETWEEN ? AND ? ORDER BY s.data DESC
        """
        self.cursor.execute(sql, (d_ini, d_fim))
        return self.cursor.fetchall()

    def excluir_peca(self, pid):
        # Busca IDs de saídas para apagar vendas órfãs
        self.cursor.execute("SELECT id FROM saidas WHERE peca_id=?", (pid,))
        rows = self.cursor.fetchall()
        s_ids = [r[0] for r in rows]
        
        if s_ids:
            placeholders = ','.join('?' * len(s_ids))
            self.cursor.execute(f"DELETE FROM vendas WHERE saida_id IN ({placeholders})", s_ids)
            
        self.cursor.execute("DELETE FROM entradas WHERE peca_id=?", (pid,))
        self.cursor.execute("DELETE FROM saidas WHERE peca_id=?", (pid,))
        self.cursor.execute("DELETE FROM pecas WHERE id=?", (pid,))
        self.conn.commit()

    def excluir_movimento(self, tabela, mid):
        if tabela == 'saidas':
            self.cursor.execute("DELETE FROM vendas WHERE saida_id=?", (mid,))
        self.cursor.execute(f"DELETE FROM {tabela} WHERE id=?", (mid,))
        self.conn.commit()