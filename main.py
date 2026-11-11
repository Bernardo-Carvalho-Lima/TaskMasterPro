import tkinter as tk

try:
    from views.tela_tarefas import TelaTarefas
except ModuleNotFoundError:  # pragma: no cover
    from TaskMasterPro.views.tela_tarefas import TelaTarefas


def main():
    root = tk.Tk()
    TelaTarefas(root)
    root.mainloop()


if __name__ == "__main__":
    main()
