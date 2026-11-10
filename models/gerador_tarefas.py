from pathlib import Path
import pandas as pd


class GeradorTarefas:
    """Modelo responsável por armazenar e recuperar as tarefas em CSV."""

    COLUNAS = ["ID", "Título", "Categoria", "Prioridade", "Prazo", "Status"]

    def __init__(self):
        raiz_projeto = Path(__file__).resolve().parent.parent
        pasta_dados = raiz_projeto / "dados"
        pasta_dados.mkdir(parents=True, exist_ok=True)
        self.arquivo = pasta_dados / "tarefas.csv"

        if not self.arquivo.exists():
            pd.DataFrame(columns=self.COLUNAS).to_csv(
                self.arquivo, index=False, encoding="utf-8-sig"
            )

    def carregar_tarefas(self):
        try:
            df = pd.read_csv(self.arquivo, encoding="utf-8-sig")
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=self.COLUNAS)

        # Mantém compatibilidade com um CSV criado por uma versão anterior.
        for coluna in self.COLUNAS:
            if coluna not in df.columns:
                df[coluna] = ""
        return df[self.COLUNAS]

    def salvar_tarefas(self, df):
        df[self.COLUNAS].to_csv(
            self.arquivo, index=False, encoding="utf-8-sig"
        )

    def adicionar_tarefa(self, titulo, categoria, prioridade, prazo):
        df = self.carregar_tarefas()
        ids = pd.to_numeric(df["ID"], errors="coerce").dropna()
        novo_id = int(ids.max()) + 1 if not ids.empty else 1

        nova_tarefa = {
            "ID": novo_id,
            "Título": titulo,
            "Categoria": categoria,
            "Prioridade": prioridade,
            "Prazo": prazo,
            "Status": "Pendente",
        }
        df = pd.concat([df, pd.DataFrame([nova_tarefa])], ignore_index=True)
        self.salvar_tarefas(df)

    def concluir_tarefa(self, tarefa_id):
        df = self.carregar_tarefas()
        df.loc[pd.to_numeric(df["ID"], errors="coerce") == tarefa_id, "Status"] = "Concluída"
        self.salvar_tarefas(df)

    def excluir_tarefa(self, tarefa_id):
        df = self.carregar_tarefas()
        df = df[pd.to_numeric(df["ID"], errors="coerce") != tarefa_id]
        self.salvar_tarefas(df)
