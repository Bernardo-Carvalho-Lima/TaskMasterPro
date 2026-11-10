import matplotlib.pyplot as plt
from models.gerador_tarefas import GeradorTarefas


class ControladorTarefas:
    """Controlador que conecta a interface ao modelo."""

    def __init__(self):
        self.modelo = GeradorTarefas()

    def adicionar(self, titulo, categoria, prioridade, prazo):
        self.modelo.adicionar_tarefa(titulo, categoria, prioridade, prazo)

    def concluir(self, tarefa_id):
        self.modelo.concluir_tarefa(tarefa_id)

    def excluir(self, tarefa_id):
        self.modelo.excluir_tarefa(tarefa_id)

    def listar(self):
        return self.modelo.carregar_tarefas()

    def gerar_grafico(self, tipo="Status"):
        df = self.listar()
        if df.empty:
            return False

        if tipo == "Categoria":
            dados = df["Categoria"].value_counts()
            titulo = "Tarefas por categoria"
        else:
            dados = df["Status"].value_counts()
            titulo = "Produtividade por status"

        if dados.empty:
            return False

        plt.figure(figsize=(7, 5))
        if tipo == "Categoria":
            plt.bar(dados.index.astype(str), dados.values)
            plt.ylabel("Quantidade de tarefas")
            plt.xlabel("Categoria")
        else:
            plt.pie(dados, labels=dados.index, autopct="%1.1f%%", startangle=90)
            plt.axis("equal")

        plt.title(titulo)
        plt.tight_layout()
        plt.show()
        return True
