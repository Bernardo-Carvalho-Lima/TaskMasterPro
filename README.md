# TaskMaster Pro

Aplicativo desktop para gerenciamento de tarefas, desenvolvido em Python com Tkinter,
Pandas, Matplotlib e arquitetura MVC.

## Requisitos
- Python 3.10 ou superior
- Tkinter (normalmente incluído na instalação do Python)
- Pandas
- Matplotlib

## Como abrir e executar no VS Code

1. Extraia o arquivo ZIP.
2. Abra o VS Code e selecione **Arquivo > Abrir Pasta**.
3. Escolha a pasta `TaskMasterPro`.
4. Abra o terminal integrado (`Terminal > Novo Terminal`).
5. (Opcional, recomendado) Crie e ative um ambiente virtual:

   **Windows**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

6. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

7. Execute:
   ```bash
   python main.py
   ```

## Funcionalidades
- Cadastro de tarefas com título, categoria, prioridade e prazo.
- Status pendente/concluída.
- Salvamento automático em `dados/tarefas.csv`.
- Listagem em tabela.
- Indicadores de total, concluídas e pendentes.
- Gráfico de produtividade por status ou categoria.
- Marcar tarefas como concluídas e excluir tarefas.

## Estrutura MVC
- `models/`: leitura, gravação e regras de persistência dos dados.
- `controllers/`: operações entre a interface e o modelo.
- `views/`: interface gráfica Tkinter.
- `dados/`: arquivo CSV de persistência.
- `main.py`: ponto de entrada da aplicação.
