import tkinter as tk
from datetime import date, datetime
from ..database.queries import listar_para_alertas
from ..utils.estilos import (COR_BG, COR_CARD, COR_BORDA, COR_ACENTO,
                              COR_TEXTO, COR_SUBTEXTO, COR_VERDE, COR_VERMELHO, COR_AMARELO,
                              FONTE_TITULO, FONTE_SUBTIT, FONTE_NORMAL, FONTE_SMALL, FONTE_BOLD)


class FrameAlertas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COR_BG)
        tk.Label(self, text="🔔  Alertas de Vencimento",
                 font=FONTE_TITULO, bg=COR_BG, fg=COR_ACENTO).pack(anchor="w", pady=(0, 16))

        self.container = tk.Frame(self, bg=COR_BG)
        self.container.pack(fill="both", expand=True)

    def atualizar(self):
        for w in self.container.winfo_children():
            w.destroy()

        rows  = listar_para_alertas()
        hoje  = date.today()
        grupos = {"atrasados": [], "hoje": [], "7dias": [], "ok": []}

        for nome, sol, setor, dt_dev in rows:
            d    = datetime.strptime(dt_dev, "%Y-%m-%d").date()
            dias = (d - hoje).days
            item = (nome, sol, setor, d, dias)
            if dias < 0:
                grupos["atrasados"].append(item)
            elif dias == 0:
                grupos["hoje"].append(item)
            elif dias <= 7:
                grupos["7dias"].append(item)
            else:
                grupos["ok"].append(item)

        secoes = [
            ("atrasados", "🚨  Atrasados",                  COR_VERMELHO, grupos["atrasados"]),
            ("hoje",      "⚠️  Vencem Hoje",                COR_AMARELO,  grupos["hoje"]),
            ("7dias",     "📅  Vencem nos Próximos 7 Dias", "#fb923c",    grupos["7dias"]),
            ("ok",        "✅  Em Dia",                     COR_VERDE,    grupos["ok"]),
        ]

        tem_algum = False
        for _, titulo, cor, itens in secoes:
            if not itens:
                continue
            tem_algum = True
            tk.Label(self.container, text=f"{titulo} ({len(itens)})",
                     font=FONTE_SUBTIT, bg=COR_BG, fg=cor).pack(anchor="w", pady=(12, 4))

            for nome, sol, setor, d, dias in itens:
                card = tk.Frame(self.container, bg=COR_CARD, highlightthickness=1,
                                highlightbackground=cor)
                card.pack(fill="x", pady=2)
                inner = tk.Frame(card, bg=COR_CARD, padx=16, pady=10)
                inner.pack(fill="x")

                tk.Label(inner, text=nome, font=FONTE_BOLD,
                         bg=COR_CARD, fg=COR_TEXTO).pack(side="left")

                if dias < 0:
                    msg = f"Atrasado {abs(dias)} dia(s)"
                elif dias == 0:
                    msg = "Vence hoje!"
                else:
                    msg = f"Vence em {dias} dia(s)"

                tk.Label(inner, text=msg, font=FONTE_SMALL,
                         bg=COR_CARD, fg=cor).pack(side="left", padx=16)

                tk.Label(inner,
                         text=f"Solicitante: {sol} | Setor: {setor or '-'} | Devolução: {d.strftime('%d/%m/%Y')}",
                         font=FONTE_SMALL, bg=COR_CARD, fg=COR_SUBTEXTO).pack(side="left")

        if not tem_algum:
            tk.Label(self.container, text="Nenhum documento emprestado no momento.",
                     font=FONTE_NORMAL, bg=COR_BG, fg=COR_SUBTEXTO).pack(pady=40)
