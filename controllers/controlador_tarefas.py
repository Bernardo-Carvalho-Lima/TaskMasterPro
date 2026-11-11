from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

try:
    from models.gerador_tarefas import GeradorTarefas
except ModuleNotFoundError:  # pragma: no cover
    from TaskMasterPro.models.gerador_tarefas import GeradorTarefas


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

    def gerar_dashboard(self):
        df = self.listar()
        if df.empty:
            return {
                "total": 0,
                "concluidas": 0,
                "pendentes": 0,
                "status": {},
                "categorias": {},
                "prioridades": {},
            }

        status = df["Status"].value_counts().sort_index()
        categorias = df["Categoria"].value_counts().sort_index()
        prioridades = df["Prioridade"].value_counts().sort_index()

        return {
            "total": int(len(df)),
            "concluidas": int((df["Status"] == "Concluída").sum()),
            "pendentes": int((df["Status"] == "Pendente").sum()),
            "status": {str(chave): int(valor) for chave, valor in status.items()},
            "categorias": {str(chave): int(valor) for chave, valor in categorias.items()},
            "prioridades": {str(chave): int(valor) for chave, valor in prioridades.items()},
        }

    def exportar_para_power_bi(self, caminho=None):
        df = self.listar().copy()
        if df.empty:
            df = pd.DataFrame(columns=["ID", "Título", "Categoria", "Prioridade", "Prazo", "Status"])

        df["Status_Concluida"] = df["Status"].eq("Concluída").astype(int)
        df["Prazo_Convertido"] = pd.to_datetime(df["Prazo"], format="%d/%m/%Y", errors="coerce")
        df["Prazo_Vencido"] = (
            df["Prazo_Convertido"] < pd.Timestamp.now().normalize()
        ) & df["Status"].ne("Concluída")
        df["Prazo_Vencido"] = df["Prazo_Vencido"].astype(int)

        if caminho is None:
            pasta = Path(__file__).resolve().parent.parent / "dados"
            pasta.mkdir(parents=True, exist_ok=True)
            caminho = pasta / "powerbi_tarefas.csv"

        caminho = Path(caminho)
        df.to_csv(caminho, index=False, encoding="utf-8-sig")
        return str(caminho)

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
            plt.bar(dados.index.astype(str), dados.values, color="#4F7BFF")
            plt.ylabel("Quantidade de tarefas")
            plt.xlabel("Categoria")
        else:
            plt.pie(dados, labels=dados.index, autopct="%1.1f%%", startangle=90)
            plt.axis("equal")

        plt.title(titulo)
        plt.tight_layout()
        plt.show()
        return True
