import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "licitacao_docs.db")

def get_conn():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Cria as tabelas do banco se ainda não existirem."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_documento      TEXT NOT NULL,
            numero_processo     TEXT,
            solicitante         TEXT NOT NULL,
            setor               TEXT,
            data_emprestimo     TEXT NOT NULL,
            data_devolucao      TEXT NOT NULL,
            status              TEXT DEFAULT 'Emprestado',
            observacoes         TEXT,
            data_devolucao_real TEXT
        )
    """)
    conn.commit()
    conn.close()
