# main.py - Punto de entrada de la aplicación Muertos y Heridos.

import tkinter as tk
from gui import crear_interfaz

if __name__ == "__main__":
    raiz = tk.Tk()
    crear_interfaz(raiz)
    raiz.mainloop()
