# 📋 DocControl — Controle de Documentos para Licitação

![Status](https://img.shields.io/badge/status-concluído-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

> Sistema desktop de controle de empréstimo de documentos para o setor de licitação.
> Interface gráfica em Python com alertas de prazo, histórico de devoluções e busca/filtros.

---

## 🖥️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.8+ | Linguagem principal |
| Tkinter | Interface gráfica (GUI) |
| SQLite3 | Banco de dados local |
| ttk (Tkinter) | Componentes visuais (tabelas, combobox) |

> Nenhuma biblioteca externa necessária — tudo já vem com o Python!

---

## 📁 Estrutura do Projeto

```
doccontrol_projeto/
│
├── main.py                        ← Ponto de entrada — execute este arquivo
├── licitacao_docs.db              ← Banco de dados (criado automaticamente)
│
└── doccontrol/
    ├── database/
    │   ├── connection.py          ← Conexão e criação das tabelas
    │   └── queries.py             ← Operações: inserir, buscar, devolver, excluir
    │
    ├── ui/
    │   ├── app.py                 ← Janela principal + sidebar + navegação
    │   ├── frame_emprestar.py     ← Tela de registrar empréstimo
    │   ├── frame_lista.py         ← Tela de documentos emprestados
    │   ├── frame_alertas.py       ← Tela de alertas de vencimento
    │   ├── frame_historico.py     ← Tela de histórico de devoluções
    │   └── janela_editar.py       ← Pop-up de edição de registro
    │
    └── utils/
        └── estilos.py             ← Cores, fontes e estilos visuais
```

---

## ✨ Funcionalidades

- **📤 Registrar Empréstimo** — Cadastre documentos com nome, nº de processo, solicitante, setor e prazo de devolução
- **📋 Documentos Emprestados** — Visualize todos os documentos ativos com destaque por cor:
  - 🔴 Vermelho = Atrasado
  - 🟡 Amarelo = Vence hoje
  - ⚪ Normal = Em dia
- **🔍 Busca e Filtros** — Pesquisa em tempo real por nome, solicitante ou processo
- **🔔 Alertas de Vencimento** — Pop-up automático ao abrir o sistema com documentos vencidos
- **📜 Histórico de Devoluções** — Registro completo com indicação de pontualidade
- **✏️ Editar / Excluir** — Gerencie os registros existentes

---

## ▶️ Como Rodar

### 1. Pré-requisitos

Tenha o **Python 3.8 ou superior** instalado. Para verificar, abra o terminal e digite:

```bash
python --version
```

### 2. Clone o repositório

```bash
git clone https://github.com/GeorgeNascimento/doccontrol.git
cd doccontrol
```

### 3. Execute o sistema

```bash
python main.py
```

> ⚠️ Certifique-se de rodar o comando **dentro da pasta `doccontrol_projeto`**, onde o arquivo `main.py` está localizado.

O banco de dados `licitacao_docs.db` será criado automaticamente na primeira execução.

---

## 💡 Observações

- O sistema funciona **100% offline** — nenhuma conexão com internet é necessária
- Os dados ficam salvos no arquivo `licitacao_docs.db` na mesma pasta do projeto
- Para fazer **backup**, basta copiar esse arquivo `.db`

---

## 📌 Próximas Melhorias Planejadas

- [ ] Notificações nativas do Windows (system tray)
- [ ] Envio de e-mail automático para documentos atrasados
- [ ] Exportação de relatórios em Excel/PDF
- [ ] Renovação de prazo com histórico
- [ ] Login com usuário e senha

---

## 👨‍💻 Autor

Desenvolvido para uso interno no setor de licitação.

George Guedes