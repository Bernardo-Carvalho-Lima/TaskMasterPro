import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

try:
    from controllers.controlador_tarefas import ControladorTarefas
except ModuleNotFoundError:  # pragma: no cover
    from TaskMasterPro.controllers.controlador_tarefas import ControladorTarefas


class TelaDashboard(tk.Toplevel):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.title("Dashboard - TaskMaster Pro")
        self.geometry("980x680")
        self.minsize(860, 560)
        self.controlador = controlador
        self.criar_componentes()
        self.atualizar_dashboard()

    def criar_componentes(self):
        self.frame_kpis = ttk.Frame(self, padding=10)
        self.frame_kpis.pack(fill=tk.X)

        self.kpi_total = ttk.Label(self.frame_kpis, text="Total: 0", font=("Arial", 12, "bold"))
        self.kpi_total.pack(side=tk.LEFT, expand=True)
        self.kpi_concluidas = ttk.Label(self.frame_kpis, text="Concluídas: 0", font=("Arial", 12, "bold"))
        self.kpi_concluidas.pack(side=tk.LEFT, expand=True)
        self.kpi_pendentes = ttk.Label(self.frame_kpis, text="Pendentes: 0", font=("Arial", 12, "bold"))
        self.kpi_pendentes.pack(side=tk.LEFT, expand=True)

        self.frame_graficos = ttk.Frame(self)
        self.frame_graficos.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.ax_status = self.fig.add_subplot(121)
        self.ax_categoria = self.fig.add_subplot(122)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_graficos)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def atualizar_dashboard(self):
        dados = self.controlador.gerar_dashboard()

        self.kpi_total.config(text=f"Total: {dados['total']}")
        self.kpi_concluidas.config(text=f"Concluídas: {dados['concluidas']}")
        self.kpi_pendentes.config(text=f"Pendentes: {dados['pendentes']}")

        self.ax_status.clear()
        status = dados["status"]
        if status:
            self.ax_status.bar(list(status.keys()), list(status.values()), color=["#4CAF50", "#FF9800"])
            self.ax_status.set_title("Status das tarefas")
            self.ax_status.set_xlabel("Status")
            self.ax_status.set_ylabel("Quantidade")
        else:
            self.ax_status.text(0.5, 0.5, "Sem tarefas", ha="center", va="center")
            self.ax_status.set_axis_off()

        self.ax_categoria.clear()
        categorias = dados["categorias"]
        if categorias:
            self.ax_categoria.bar(list(categorias.keys()), list(categorias.values()), color="#5C6BC0")
            self.ax_categoria.set_title("Tarefas por categoria")
            self.ax_categoria.set_xlabel("Categoria")
            self.ax_categoria.set_ylabel("Quantidade")
        else:
            self.ax_categoria.text(0.5, 0.5, "Sem categorias", ha="center", va="center")
            self.ax_categoria.set_axis_off()

        self.fig.tight_layout()
        self.canvas.draw()


class TelaTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster Pro")
        self.root.geometry("1050x650")
        self.root.minsize(850, 550)

        self.controlador = ControladorTarefas()
        self.criar_componentes()
        self.carregar_tabela()

    def criar_componentes(self):
        titulo = ttk.Label(
            self.root, text="TaskMaster Pro", font=("Arial", 20, "bold")
        )
        titulo.pack(pady=(15, 5))

        frame_form = ttk.LabelFrame(self.root, text="Cadastrar tarefa", padding=12)
        frame_form.pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(frame_form, text="Título").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_titulo = ttk.Entry(frame_form, width=27)
        self.entry_titulo.grid(row=1, column=0, padx=5, pady=5)

        ttk.Label(frame_form, text="Categoria").grid(row=0, column=1, sticky="w", padx=5)
        self.combo_categoria = ttk.Combobox(
            frame_form, values=["Trabalho", "Estudos", "Pessoal"],
            state="readonly", width=17
        )
        self.combo_categoria.grid(row=1, column=1, padx=5, pady=5)
        self.combo_categoria.set("Estudos")

        ttk.Label(frame_form, text="Prioridade").grid(row=0, column=2, sticky="w", padx=5)
        self.combo_prioridade = ttk.Combobox(
            frame_form, values=["Baixa", "Média", "Alta"],
            state="readonly", width=13
        )
        self.combo_prioridade.grid(row=1, column=2, padx=5, pady=5)
        self.combo_prioridade.set("Média")

        ttk.Label(frame_form, text="Prazo (DD/MM/AAAA)").grid(
            row=0, column=3, sticky="w", padx=5
        )
        self.entry_prazo = ttk.Entry(frame_form, width=17)
        self.entry_prazo.grid(row=1, column=3, padx=5, pady=5)
        self.entry_prazo.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ttk.Button(
            frame_form, text="Adicionar Tarefa", command=self.adicionar_tarefa
        ).grid(row=1, column=4, padx=10)

        frame_kpis = ttk.Frame(self.root)
        frame_kpis.pack(fill=tk.X, padx=15, pady=8)

        self.kpi_total = ttk.Label(frame_kpis, text="Total: 0", font=("Arial", 12, "bold"))
        self.kpi_total.pack(side=tk.LEFT, expand=True)
        self.kpi_concluidas = ttk.Label(
            frame_kpis, text="Concluídas: 0", font=("Arial", 12, "bold")
        )
        self.kpi_concluidas.pack(side=tk.LEFT, expand=True)
        self.kpi_pendentes = ttk.Label(
            frame_kpis, text="Pendentes: 0", font=("Arial", 12, "bold")
        )
        self.kpi_pendentes.pack(side=tk.LEFT, expand=True)

        frame_tabela = ttk.Frame(self.root)
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        colunas = ("ID", "Título", "Categoria", "Prioridade", "Prazo", "Status")
        self.tree = ttk.Treeview(
            frame_tabela, columns=colunas, show="headings", height=14
        )
        larguras = {
            "ID": 50, "Título": 300, "Categoria": 130,
            "Prioridade": 110, "Prazo": 120, "Status": 130
        }
        for coluna in colunas:
            self.tree.heading(coluna, text=coluna)
            self.tree.column(coluna, width=larguras[coluna], anchor=tk.CENTER)

        barra = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=barra.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        barra.pack(side=tk.RIGHT, fill=tk.Y)

        frame_botoes = ttk.Frame(self.root)
        frame_botoes.pack(pady=(0, 15))

        ttk.Button(
            frame_botoes, text="Marcar como Concluída",
            command=self.concluir_tarefa
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            frame_botoes, text="Excluir Tarefa",
            command=self.excluir_tarefa
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            frame_botoes, text="Dashboard",
            command=self.abrir_dashboard
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            frame_botoes, text="Gráfico por Status",
            command=lambda: self.gerar_grafico("Status")
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            frame_botoes, text="Gráfico por Categoria",
            command=lambda: self.gerar_grafico("Categoria")
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            frame_botoes, text="Exportar para Power BI",
            command=self.exportar_power_bi
        ).pack(side=tk.LEFT, padx=6)

    def atualizar_kpis(self):
        df = self.controlador.listar()
        total = len(df)
        concluidas = (df["Status"] == "Concluída").sum()
        pendentes = (df["Status"] == "Pendente").sum()

        self.kpi_total.config(text=f"Total: {total}")
        self.kpi_concluidas.config(text=f"Concluídas: {concluidas}")
        self.kpi_pendentes.config(text=f"Pendentes: {pendentes}")

    def carregar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        df = self.controlador.listar()
        for _, linha in df.iterrows():
            valores = [linha[coluna] for coluna in self.tree["columns"]]
            self.tree.insert("", tk.END, values=valores)

        self.atualizar_kpis()

    def adicionar_tarefa(self):
        titulo = self.entry_titulo.get().strip()
        categoria = self.combo_categoria.get()
        prioridade = self.combo_prioridade.get()
        prazo = self.entry_prazo.get().strip()

        if not titulo:
            messagebox.showwarning("Atenção", "Digite o título da tarefa.")
            self.entry_titulo.focus()
            return
        if not categoria or not prioridade:
            messagebox.showwarning("Atenção", "Selecione a categoria e a prioridade.")
            return
        try:
            datetime.strptime(prazo, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning(
                "Prazo inválido", "Informe o prazo no formato DD/MM/AAAA."
            )
            self.entry_prazo.focus()
            return

        self.controlador.adicionar(titulo, categoria, prioridade, prazo)
        self.carregar_tabela()
        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.focus()

    def obter_id_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Seleção", "Selecione uma tarefa na tabela.")
            return None
        return int(self.tree.item(selecionado[0], "values")[0])

    def concluir_tarefa(self):
        tarefa_id = self.obter_id_selecionado()
        if tarefa_id is not None:
            self.controlador.concluir(tarefa_id)
            self.carregar_tabela()

    def excluir_tarefa(self):
        tarefa_id = self.obter_id_selecionado()
        if tarefa_id is not None:
            if messagebox.askyesno("Confirmar exclusão", "Deseja excluir esta tarefa?"):
                self.controlador.excluir(tarefa_id)
                self.carregar_tabela()

    def abrir_dashboard(self):
        TelaDashboard(self.root, self.controlador)

    def exportar_power_bi(self):
        caminho = self.controlador.exportar_para_power_bi()
        messagebox.showinfo(
            "Power BI",
            f"Arquivo exportado com sucesso:\n{caminho}",
        )

    def gerar_grafico(self, tipo):
        if not self.controlador.gerar_grafico(tipo):
            messagebox.showinfo("Sem dados", "Cadastre ao menos uma tarefa para gerar o gráfico.")
