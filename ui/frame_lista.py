import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ..database.queries import listar_emprestados, registrar_devolucao, excluir_documento, buscar_por_id
from ..utils.estilos import (COR_BG, COR_CARD, COR_BORDA, COR_ACENTO, COR_ACENTO2,
                              COR_TEXTO, COR_SUBTEXTO, COR_VERDE, COR_VERMELHO, COR_ROXO,
                              FONTE_TITULO, FONTE_NORMAL, FONTE_SMALL, FONTE_BOLD,
                              aplicar_estilo_treeview)
from .janela_editar import JanelaEditar


class FrameLista(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COR_BG)
        aplicar_estilo_treeview()
        self._build()

    def _build(self):
        tk.Label(self, text="📋  Documentos Emprestados",
                 font=FONTE_TITULO, bg=COR_BG, fg=COR_ACENTO).pack(anchor="w", pady=(0, 12))

        # Barra de busca e filtro
        busca_f = tk.Frame(self, bg=COR_CARD, highlightthickness=1,
                           highlightbackground=COR_BORDA)
        busca_f.pack(fill="x", pady=(0, 10))
        ib = tk.Frame(busca_f, bg=COR_CARD, pady=10, padx=14)
        ib.pack(fill="x")

        tk.Label(ib, text="🔍", font=("Segoe UI", 12), bg=COR_CARD, fg=COR_SUBTEXTO).pack(side="left")
        self.busca_var = tk.StringVar()
        self.busca_var.trace("w", lambda *a: self.atualizar())
        tk.Entry(ib, textvariable=self.busca_var, font=FONTE_NORMAL, bg=COR_CARD,
                 fg=COR_TEXTO, insertbackground=COR_TEXTO, relief="flat",
                 width=40).pack(side="left", padx=8, ipady=4)

        tk.Label(ib, text="Filtrar por status:", font=FONTE_SMALL,
                 bg=COR_CARD, fg=COR_SUBTEXTO).pack(side="left", padx=(20, 6))
        self.filtro_status = ttk.Combobox(ib,
                                          values=["Todos", "Emprestado", "Devolvido", "Atrasado"],
                                          width=14, font=FONTE_SMALL, state="readonly")
        self.filtro_status.set("Todos")
        self.filtro_status.bind("<<ComboboxSelected>>", lambda e: self.atualizar())
        self.filtro_status.pack(side="left")

        # Tabela
        cols = ("ID", "Documento", "Processo", "Solicitante", "Setor",
                "Emprestado em", "Devolução", "Status")
        tree_f = tk.Frame(self, bg=COR_CARD, highlightthickness=1,
                          highlightbackground=COR_BORDA)
        tree_f.pack(fill="both", expand=True)

        scroll = ttk.Scrollbar(tree_f, orient="vertical")
        scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_f, columns=cols, show="headings",
                                 yscrollcommand=scroll.set, style="Custom.Treeview")
        scroll.config(command=self.tree.yview)

        larg = [40, 200, 120, 160, 120, 110, 110, 90]
        for col, w in zip(cols, larg):
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=w, minwidth=40, anchor="w")

        self.tree.tag_configure("atrasado",   foreground=COR_VERMELHO)
        self.tree.tag_configure("vence_hoje", foreground="#f59e0b")
        self.tree.tag_configure("devolvido",  foreground=COR_VERDE)
        self.tree.pack(fill="both", expand=True)

        # Botões
        btn_bar = tk.Frame(self, bg=COR_BG)
        btn_bar.pack(fill="x", pady=(10, 0))

        tk.Button(btn_bar, text="✔  Registrar Devolução",
                  font=FONTE_NORMAL, bg=COR_VERDE, fg="white",
                  activebackground="#16a34a", bd=0, pady=8, padx=16,
                  cursor="hand2", command=self._devolver).pack(side="left")

        tk.Button(btn_bar, text="✏  Editar",
                  font=FONTE_NORMAL, bg=COR_ROXO, fg="white",
                  activebackground="#7c3aed", bd=0, pady=8, padx=16,
                  cursor="hand2", command=self._editar).pack(side="left", padx=8)

        tk.Button(btn_bar, text="🗑  Excluir",
                  font=FONTE_NORMAL, bg=COR_VERMELHO, fg="white",
                  activebackground="#dc2626", bd=0, pady=8, padx=16,
                  cursor="hand2", command=self._excluir).pack(side="left")

        tk.Button(btn_bar, text="🔄  Atualizar",
                  font=FONTE_NORMAL, bg=COR_BORDA, fg=COR_SUBTEXTO,
                  activebackground=COR_CARD, bd=0, pady=8, padx=16,
                  cursor="hand2", command=self.atualizar).pack(side="right")

    def atualizar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        busca  = self.busca_var.get().strip()
        filtro = self.filtro_status.get()
        rows   = listar_emprestados(busca, filtro)

        for id_, nome, proc, sol, setor, dt_emp, dt_dev_d, status_real in rows:
            if "Atrasado" in status_real:
                tag = "atrasado"
            elif "hoje" in status_real:
                tag = "vence_hoje"
            else:
                tag = ""

            self.tree.insert("", "end", iid=id_, tags=(tag,), values=(
                id_, nome, proc or "-", sol, setor or "-",
                datetime.strptime(dt_emp, "%Y-%m-%d").strftime("%d/%m/%Y"),
                dt_dev_d.strftime("%d/%m/%Y"),
                status_real,
            ))

    def _devolver(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecione", "Selecione um documento para registrar a devolução.")
            return
        doc_id = sel[0]
        nome = self.tree.item(doc_id, "values")[1]
        if messagebox.askyesno("Confirmar", f"Registrar devolução de:\n\n'{nome}'?"):
            registrar_devolucao(doc_id)
            messagebox.showinfo("Sucesso", "Devolução registrada!")
            self.atualizar()

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecione", "Selecione um documento para excluir.")
            return
        doc_id = sel[0]
        nome = self.tree.item(doc_id, "values")[1]
        if messagebox.askyesno("Excluir", f"Excluir permanentemente '{nome}'?"):
            excluir_documento(doc_id)
            self.atualizar()

    def _editar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecione", "Selecione um documento para editar.")
            return
        row = buscar_por_id(sel[0])
        if row:
            JanelaEditar(self, row, self.atualizar)
