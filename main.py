import tkinter as tk
from views.tela_tarefas import TelaTarefas


def main():
    root = tk.Tk()
    TelaTarefas(root)
    root.mainloop()


if __name__ == "__main__":
    main()
