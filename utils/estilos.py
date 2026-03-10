from tkinter import ttk

# ── Paleta de cores ────────────────────────────────────────
COR_BG       = "#0f1923"
COR_CARD     = "#182230"
COR_BORDA    = "#1e3048"
COR_ACENTO   = "#00b4d8"
COR_ACENTO2  = "#0077a8"
COR_TEXTO    = "#e0eaf5"
COR_SUBTEXTO = "#7a9bbf"
COR_VERDE    = "#22c55e"
COR_AMARELO  = "#f59e0b"
COR_VERMELHO = "#ef4444"
COR_ROXO     = "#8b5cf6"

# ── Fontes ─────────────────────────────────────────────────
FONTE_TITULO = ("Segoe UI", 18, "bold")
FONTE_SUBTIT = ("Segoe UI", 11, "bold")
FONTE_NORMAL = ("Segoe UI", 10)
FONTE_SMALL  = ("Segoe UI", 9)
FONTE_BOLD   = ("Segoe UI", 10, "bold")


def aplicar_estilo_treeview():
    """Aplica o tema escuro nas tabelas ttk.Treeview."""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=COR_CARD,
                    fieldbackground=COR_CARD,
                    foreground=COR_TEXTO,
                    font=FONTE_NORMAL,
                    rowheight=32,
                    borderwidth=0)
    style.configure("Custom.Treeview.Heading",
                    background=COR_BORDA,
                    foreground=COR_ACENTO,
                    font=FONTE_BOLD,
                    borderwidth=0)
    style.map("Custom.Treeview",
              background=[("selected", COR_ACENTO2)])
