from datetime import date, datetime
from .connection import get_conn


def inserir_documento(nome, processo, solicitante, setor, data_devolucao, observacoes):
    """Insere um novo empréstimo no banco."""
    conn = get_conn()
    conn.execute("""
        INSERT INTO documentos
            (nome_documento, numero_processo, solicitante, setor,
             data_emprestimo, data_devolucao, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nome, processo, solicitante, setor,
        date.today().strftime("%Y-%m-%d"),
        data_devolucao.strftime("%Y-%m-%d"),
        observacoes,
    ))
    conn.commit()
    conn.close()


def listar_emprestados(busca="", status_filtro="Todos"):
    """Retorna documentos ainda não devolvidos, com filtros opcionais."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, nome_documento, numero_processo, solicitante, setor,
               data_emprestimo, data_devolucao, status
        FROM documentos
        WHERE status != 'Devolvido'
        ORDER BY data_devolucao ASC
    """).fetchall()
    conn.close()

    hoje = date.today()
    resultado = []
    for r in rows:
        id_, nome, proc, sol, setor, dt_emp, dt_dev, status = r
        dt_dev_d = datetime.strptime(dt_dev, "%Y-%m-%d").date()
        dias = (dt_dev_d - hoje).days

        if dias < 0:
            status_real = "Atrasado"
        elif dias == 0:
            status_real = "Vence hoje"
        else:
            status_real = status

        if status_filtro != "Todos" and status_filtro.lower() not in status_real.lower():
            continue
        if busca and busca.lower() not in (nome + sol + (proc or "") + (setor or "")).lower():
            continue

        resultado.append((id_, nome, proc, sol, setor, dt_emp, dt_dev_d, status_real))
    return resultado


def listar_historico(busca=""):
    """Retorna documentos já devolvidos."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, nome_documento, numero_processo, solicitante,
               data_emprestimo, data_devolucao, data_devolucao_real
        FROM documentos
        WHERE status = 'Devolvido'
        ORDER BY data_devolucao_real DESC
    """).fetchall()
    conn.close()

    resultado = []
    for r in rows:
        id_, nome, proc, sol, dt_emp, dt_dev, dt_real = r
        if busca and busca.lower() not in (nome + sol + (proc or "")).lower():
            continue
        resultado.append(r)
    return resultado


def registrar_devolucao(doc_id):
    """Marca um documento como devolvido."""
    conn = get_conn()
    conn.execute("""
        UPDATE documentos
        SET status = 'Devolvido', data_devolucao_real = ?
        WHERE id = ?
    """, (date.today().strftime("%Y-%m-%d"), doc_id))
    conn.commit()
    conn.close()


def atualizar_documento(doc_id, nome, processo, solicitante, setor, data_devolucao, observacoes):
    """Atualiza os dados de um documento existente."""
    conn = get_conn()
    conn.execute("""
        UPDATE documentos
        SET nome_documento = ?, numero_processo = ?, solicitante = ?,
            setor = ?, data_devolucao = ?, observacoes = ?
        WHERE id = ?
    """, (nome, processo, solicitante, setor,
          data_devolucao.strftime("%Y-%m-%d"), observacoes, doc_id))
    conn.commit()
    conn.close()


def excluir_documento(doc_id):
    """Remove permanentemente um documento."""
    conn = get_conn()
    conn.execute("DELETE FROM documentos WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()


def buscar_por_id(doc_id):
    """Retorna um documento pelo ID."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()
    conn.close()
    return row


def contar_alertas():
    """Retorna quantidade de documentos atrasados ou vencendo hoje."""
    conn = get_conn()
    count = conn.execute("""
        SELECT COUNT(*) FROM documentos
        WHERE status != 'Devolvido'
        AND date(data_devolucao) <= date('now')
    """).fetchone()[0]
    conn.close()
    return count


def listar_para_alertas():
    """Retorna todos os emprestados agrupáveis por urgência."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT nome_documento, solicitante, setor, data_devolucao
        FROM documentos
        WHERE status != 'Devolvido'
        ORDER BY data_devolucao ASC
    """).fetchall()
    conn.close()
    return rows
