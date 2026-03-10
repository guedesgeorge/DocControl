import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime, timedelta
from ..database.queries import inserir_documento
from ..utils.estilos import (COR_BG, COR_CARD, COR_BORDA, COR_ACENTO, COR_ACENTO2,
                              COR_TEXTO, COR_SUBTEXTO, FONTE_TITULO, FONTE_NORMAL,
                              FONTE_SMALL, FONTE_BOLD)


class FrameEmprestar(tk.Frame):
    def __init__(self, parent, on_salvo=None):
        super().__init__(parent, bg=COR_BG)
        self.on_salvo = on_salvo
        self._build()

    def _build(self):
        tk.Label(self, text="📤  Registrar Empréstimo",
                 font=FONTE_TITULO, bg=COR_BG, fg=COR_ACENTO).pack(anchor="w", pady=(0, 16))

        card = tk.Frame(self, bg=COR_CARD, highlightthickness=1,
                        highlightbackground=COR_BORDA)
        card.pack(fill="x")
        inner = tk.Frame(card, bg=COR_CARD, padx=30, pady=24)
        inner.pack(fill="both")

        campos = [
            ("Nome do Documento *",              "nome_doc"),
            ("Nº do Processo",                   "num_processo"),
            ("Solicitante *",                    "solicitante"),
            ("Setor / Departamento",             "setor"),
            ("Data de Devolução * (DD/MM/AAAA)", "data_dev"),
            ("Observações",                      "obs"),
        ]

        self.entradas = {}
        for label, chave in campos:
            row = tk.Frame(inner, bg=COR_CARD)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label, font=FONTE_SMALL, bg=COR_CARD,
                     fg=COR_SUBTEXTO, width=30, anchor="w").pack(side="left")
            entry = tk.Entry(row, font=FONTE_NORMAL, bg=COR_BG, fg=COR_TEXTO,
                             insertbackground=COR_TEXTO, relief="flat",
                             highlightthickness=1, highlightbackground=COR_BORDA,
                             highlightcolor=COR_ACENTO, width=40)
            entry.pack(side="left", ipady=6, padx=(8, 0))
            self.entradas[chave] = entry

        padrao = (date.today() + timedelta(days=7)).strftime("%d/%m/%Y")
        self.entradas["data_dev"].insert(0, padrao)

        tk.Frame(inner, bg=COR_BORDA, height=1).pack(fill="x", pady=16)

        btn_frame = tk.Frame(inner, bg=COR_CARD)
        btn_frame.pack(anchor="w")

        tk.Button(btn_frame, text="  Registrar Empréstimo  ",
                  font=FONTE_BOLD, bg=COR_ACENTO, fg="white",
                  activebackground=COR_ACENTO2, bd=0, pady=10, padx=20,
                  cursor="hand2", command=self._salvar).pack(side="left")

        tk.Button(btn_frame, text="  Limpar  ",
                  font=FONTE_NORMAL, bg=COR_BORDA, fg=COR_SUBTEXTO,
                  activebackground=COR_CARD, bd=0, pady=10, padx=16,
                  cursor="hand2", command=self._limpar).pack(side="left", padx=10)

    def _salvar(self):
        nome    = self.entradas["nome_doc"].get().strip()
        solicit = self.entradas["solicitante"].get().strip()
        data_d  = self.entradas["data_dev"].get().strip()

        if not nome or not solicit or not data_d:
            messagebox.showwarning("Campos obrigatórios",
                                   "Preencha Nome do Documento, Solicitante e Data de Devolução.")
            return

        try:
            dt_dev = datetime.strptime(data_d, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Data inválida", "Use o formato DD/MM/AAAA para a data.")
            return

        if dt_dev < date.today():
            if not messagebox.askyesno("Atenção", "A data de devolução já passou. Confirmar mesmo assim?"):
                return

        inserir_documento(
            nome,
            self.entradas["num_processo"].get().strip(),
            solicit,
            self.entradas["setor"].get().strip(),
            dt_dev,
            self.entradas["obs"].get().strip(),
        )

        messagebox.showinfo("Sucesso", f"Documento '{nome}' registrado com sucesso!")
        self._limpar()
        if self.on_salvo:
            self.on_salvo()

    def _limpar(self):
        for e in self.entradas.values():
            e.delete(0, tk.END)
        padrao = (date.today() + timedelta(days=7)).strftime("%d/%m/%Y")
        self.entradas["data_dev"].insert(0, padrao)
