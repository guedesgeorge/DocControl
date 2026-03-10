import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from ..database.queries import atualizar_documento
from ..utils.estilos import (COR_BG, COR_CARD, COR_BORDA, COR_ACENTO, COR_ACENTO2,
                              COR_TEXTO, COR_SUBTEXTO,
                              FONTE_TITULO, FONTE_NORMAL, FONTE_SMALL, FONTE_BOLD)


class JanelaEditar(tk.Toplevel):
    def __init__(self, parent, row, callback):
        super().__init__(parent)
        self.callback = callback
        self.doc_id   = row[0]
        self.title("Editar Documento")
        self.geometry("520x480")
        self.configure(bg=COR_BG)
        self.grab_set()
        self._build(row)

    def _build(self, row):
        tk.Label(self, text="✏  Editar Registro",
                 font=FONTE_TITULO, bg=COR_BG, fg=COR_ACENTO).pack(anchor="w", padx=24, pady=(20, 12))

        card = tk.Frame(self, bg=COR_CARD, highlightthickness=1,
                        highlightbackground=COR_BORDA)
        card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        inner = tk.Frame(card, bg=COR_CARD, padx=24, pady=20)
        inner.pack(fill="both")

        dt_dev_fmt = datetime.strptime(row[6], "%Y-%m-%d").strftime("%d/%m/%Y") if row[6] else ""

        campos = [
            ("Nome do Documento",              row[1]),
            ("Nº Processo",                    row[2] or ""),
            ("Solicitante",                    row[3]),
            ("Setor",                          row[4] or ""),
            ("Data Devolução (DD/MM/AAAA)",    dt_dev_fmt),
            ("Observações",                    row[8] or ""),
        ]
        keys = ["nome", "proc", "sol", "setor", "dev", "obs"]

        self.ent = {}
        for (lbl, val), chave in zip(campos, keys):
            row_f = tk.Frame(inner, bg=COR_CARD)
            row_f.pack(fill="x", pady=5)
            tk.Label(row_f, text=lbl, font=FONTE_SMALL, bg=COR_CARD,
                     fg=COR_SUBTEXTO, width=26, anchor="w").pack(side="left")
            e = tk.Entry(row_f, font=FONTE_NORMAL, bg=COR_BG, fg=COR_TEXTO,
                         insertbackground=COR_TEXTO, relief="flat",
                         highlightthickness=1, highlightbackground=COR_BORDA,
                         highlightcolor=COR_ACENTO, width=30)
            e.insert(0, val)
            e.pack(side="left", ipady=5, padx=(8, 0))
            self.ent[chave] = e

        tk.Button(inner, text="  Salvar Alterações  ",
                  font=FONTE_BOLD, bg=COR_ACENTO, fg="white",
                  activebackground=COR_ACENTO2, bd=0, pady=8, padx=16,
                  cursor="hand2", command=self._salvar).pack(anchor="w", pady=(14, 0))

    def _salvar(self):
        try:
            dt = datetime.strptime(self.ent["dev"].get().strip(), "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Data inválida", "Use DD/MM/AAAA", parent=self)
            return

        atualizar_documento(
            self.doc_id,
            self.ent["nome"].get().strip(),
            self.ent["proc"].get().strip(),
            self.ent["sol"].get().strip(),
            self.ent["setor"].get().strip(),
            dt,
            self.ent["obs"].get().strip(),
        )
        messagebox.showinfo("Salvo", "Registro atualizado!", parent=self)
        self.callback()
        self.destroy()
