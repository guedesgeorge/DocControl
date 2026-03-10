import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ..database.queries import listar_historico
from ..utils.estilos import (COR_BG, COR_CARD, COR_BORDA, COR_ACENTO,
                              COR_TEXTO, COR_SUBTEXTO, COR_VERDE, COR_VERMELHO,
                              FONTE_TITULO, FONTE_NORMAL, FONTE_SMALL, FONTE_BOLD,
                              aplicar_estilo_treeview)


class FrameHistorico(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COR_BG)
        aplicar_estilo_treeview()
        self._build()

    def _build(self):
        tk.Label(self, text="📜  Histórico de Devoluções",
                 font=FONTE_TITULO, bg=COR_BG, fg=COR_ACENTO).pack(anchor="w", pady=(0, 16))

        # Busca
        bf = tk.Frame(self, bg=COR_CARD, highlightthickness=1, highlightbackground=COR_BORDA)
        bf.pack(fill="x", pady=(0, 10))
        ib = tk.Frame(bf, bg=COR_CARD, pady=10, padx=14)
        ib.pack(fill="x")

        tk.Label(ib, text="🔍", font=("Segoe UI", 12), bg=COR_CARD, fg=COR_SUBTEXTO).pack(side="left")
        self.busca_var = tk.StringVar()
        self.busca_var.trace("w", lambda *a: self.atualizar())
        tk.Entry(ib, textvariable=self.busca_var, font=FONTE_NORMAL,
                 bg=COR_CARD, fg=COR_TEXTO, insertbackground=COR_TEXTO,
                 relief="flat", width=40).pack(side="left", padx=8, ipady=4)

        # Tabela
        cols = ("ID", "Documento", "Processo", "Solicitante",
                "Emprestado", "Prazo", "Devolvido em", "Pontualidade")
        tree_f = tk.Frame(self, bg=COR_CARD, highlightthickness=1, highlightbackground=COR_BORDA)
        tree_f.pack(fill="both", expand=True)

        scroll = ttk.Scrollbar(tree_f, orient="vertical")
        scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_f, columns=cols, show="headings",
                                 yscrollcommand=scroll.set, style="Custom.Treeview")
        scroll.config(command=self.tree.yview)

        larg = [40, 200, 110, 160, 100, 100, 110, 110]
        for col, w in zip(cols, larg):
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=w, minwidth=40, anchor="w")

        self.tree.tag_configure("pontual",  foreground=COR_VERDE)
        self.tree.tag_configure("atrasado", foreground=COR_VERMELHO)
        self.tree.pack(fill="both", expand=True)

    def atualizar(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        busca = self.busca_var.get().strip()
        rows  = listar_historico(busca)

        for id_, nome, proc, sol, dt_emp, dt_dev, dt_real in rows:
            d_prazo = datetime.strptime(dt_dev, "%Y-%m-%d").date()
            d_real  = datetime.strptime(dt_real, "%Y-%m-%d").date() if dt_real else None

            if d_real:
                pontual = "✅ Pontual" if d_real <= d_prazo else f"⚠ {(d_real - d_prazo).days}d atraso"
                tag     = "pontual"   if d_real <= d_prazo else "atrasado"
            else:
                pontual, tag = "-", ""

            self.tree.insert("", "end", iid=id_, tags=(tag,), values=(
                id_, nome, proc or "-", sol,
                datetime.strptime(dt_emp, "%Y-%m-%d").strftime("%d/%m/%Y"),
                d_prazo.strftime("%d/%m/%Y"),
                d_real.strftime("%d/%m/%Y") if d_real else "-",
                pontual,
            ))
