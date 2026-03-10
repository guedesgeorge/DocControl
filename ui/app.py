import tkinter as tk
from tkinter import messagebox
from ..database.connection import init_db
from ..database.queries import contar_alertas
from ..ui.frame_emprestar import FrameEmprestar
from ..ui.frame_lista     import FrameLista
from ..ui.frame_alertas   import FrameAlertas
from ..ui.frame_historico import FrameHistorico
from ..utils.estilos import (COR_BG, COR_CARD, COR_BORDA, COR_ACENTO, COR_ACENTO2,
                              COR_TEXTO, COR_SUBTEXTO, FONTE_NORMAL)


class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Controle de Documentos — Setor de Licitação")
        self.geometry("1200x720")
        self.minsize(1000, 600)
        self.configure(bg=COR_BG)

        init_db()
        self._build_sidebar()
        self._build_conteudo()
        self._mudar_aba("lista")
        self._verificar_alertas()

    # ── Sidebar ───────────────────────────────
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=COR_CARD, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Cabeçalho
        hdr = tk.Frame(self.sidebar, bg=COR_ACENTO2, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📋", font=("Segoe UI", 22),
                 bg=COR_ACENTO2, fg="white").pack(side="left", padx=12, pady=12)
        tk.Label(hdr, text="DocControl\nLicitação", font=("Segoe UI", 10, "bold"),
                 bg=COR_ACENTO2, fg="white", justify="left").pack(side="left")

        tk.Frame(self.sidebar, bg=COR_BORDA, height=1).pack(fill="x", pady=8)

        # Botões de navegação
        self._btns = {}
        nav = [
            ("📤  Emprestar Doc.", "emprestar"),
            ("📋  Documentos",     "lista"),
            ("🔔  Alertas",        "alertas"),
            ("📜  Histórico",      "historico"),
        ]
        for txt, chave in nav:
            btn = tk.Button(self.sidebar, text=txt, font=FONTE_NORMAL,
                            bg=COR_CARD, fg=COR_TEXTO, bd=0, pady=12,
                            activebackground=COR_BORDA, activeforeground=COR_ACENTO,
                            anchor="w", padx=20, cursor="hand2",
                            command=lambda c=chave: self._mudar_aba(c))
            btn.pack(fill="x")
            self._btns[chave] = btn

    # ── Área de conteúdo ──────────────────────
    def _build_conteudo(self):
        self.main = tk.Frame(self, bg=COR_BG)
        self.main.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self._frames = {
            "emprestar": FrameEmprestar(self.main, on_salvo=lambda: None),
            "lista":     FrameLista(self.main),
            "alertas":   FrameAlertas(self.main),
            "historico": FrameHistorico(self.main),
        }

    def _mudar_aba(self, chave):
        for f in self._frames.values():
            f.pack_forget()
        for k, b in self._btns.items():
            b.configure(bg=COR_CARD, fg=COR_TEXTO)

        self._btns[chave].configure(bg=COR_BORDA, fg=COR_ACENTO)
        self._frames[chave].pack(fill="both", expand=True)

        # Atualiza dados ao entrar na aba
        if chave == "lista":
            self._frames["lista"].atualizar()
        elif chave == "alertas":
            self._frames["alertas"].atualizar()
        elif chave == "historico":
            self._frames["historico"].atualizar()

    def _verificar_alertas(self):
        count = contar_alertas()
        if count > 0:
            messagebox.showwarning(
                "⚠️ Alertas de Vencimento",
                f"Há {count} documento(s) atrasado(s) ou que vencem hoje!\n\nVerifique a aba Alertas."
            )
