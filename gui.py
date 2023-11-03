import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from juego import Juego

from juego import Juego

def enviar_numero(juego, raiz, entrada_texto, mensaje_etiqueta, resultado_etiqueta, ranking_tabla):
    # Función llamada al hacer clic en el botón "Adivinar". Realiza un intento y actualiza la interfaz.
    entrada = entrada_texto.get()
    entrada_texto.delete(0, tk.END)
    reiniciar = juego.jugar(entrada, mensaje_etiqueta, resultado_etiqueta, ranking_tabla, raiz)
    if reiniciar:
        nueva_partida(juego, resultado_etiqueta, mensaje_etiqueta, ranking_tabla)

def nueva_partida(juego, resultado_etiqueta, mensaje_etiqueta, ranking_tabla):
    # Inicia una nueva partida, reiniciando el juego y limpiando la interfaz.
    juego.reiniciar_juego()
    resultado_etiqueta.config(text="")
    mensaje_etiqueta.config(text="")
    ranking_tabla.delete(*ranking_tabla.get_children())

    
def mostrar_reglas():
    # Muestra un cuadro de diálogo con las reglas del juego "Muertos y Heridos".
    reglas = """
El dispositivo piensa un número de tres o cuatro cifras (lo puedes cambiar en opciones).
Tú tienes que encontrarlo. Cada vez que dices un número el dispositivo te contesta cuántos muertos y cuántos heridos tiene tu intento.

Un ejemplo: tú escribes 1234. El dispositivo lo compara con el número oculto, el número que tú no conoces y tienes que adivinar, supongamos que es 1249. Entonces te contesta que hay 2 muertos y 1 herido. Los muertos son 1 y 2. El herido es el 4. Pero esto tú no lo sabes. Solo sabes que tu número tiene 2 cifras bien colocadas y una más que no está en su sitio. También sabes que una de tus cifras no está en el número oculto. Ahora haz otro intento.

Se considera que adivinar el número en 8 intentos es una buena marca. La mayoría de la gente necesita 10 o más intentos.
    """
    messagebox.showinfo("Las reglas abreviadas 💀", reglas)

def Historia():
    # Muestra un cuadro de diálogo con la historia del juego "Muertos y Heridos".
    historia = """
El juego de los muertos y los heridos es un juego de deducción lógica para dos o más jugadores que tradicionalmente se ha jugado usando lápiz y papel. También es llamado Picas y Fijas o Punto y Fama. También hay una antigua versión de escritorio llamada 4digits..

Me enseñaron este juego con el nombre de "juego de los Muertos y los Heridos" de pequeño y jugué con mi primo Álvaro incontables veces. Me encantaba, aunque también es verdad que no teníamos mucho más que hacer. En aquella época existía una cosa que se llamaba "tarde interminable en el campo". En cambio no existían móviles.
    """
    messagebox.showinfo("Picas y Fijas o Punto y Fama. 💀", historia)


def crear_interfaz(raiz):
    # Crea la interfaz de usuario, incluyendo botones, etiquetas y la tabla de ranking.

    def guardar_registro_partida():
        # Abre un cuadro de diálogo para guardar un archivo de registro de la partida.
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])

        if archivo:
            try:
                with open(archivo, 'w') as f:
                    for intento in juego.intentos:
                        f.write(f"Intento: {intento[0]}, Número: {intento[1]}, Muertos: {intento[2]}, Heridos: {intento[3]}\n")
            except Exception as e:
                mensaje_etiqueta.config(text=f"Error al guardar el archivo: {str(e)}")
            else:
                mensaje_etiqueta.config(text=f"Registro de partida guardado en {archivo}")


    raiz.title("Muertos y Heridos")
    raiz.configure(bg='lightblue')

    marco = tk.Frame(raiz, bg='lightblue')
    marco.pack(pady=5)

    botones_historia_reglas = tk.Frame(marco, bg='lightblue')
    botones_historia_reglas.pack(pady=5)

    boton_historia = tk.Button(botones_historia_reglas, text="Historia", command=Historia)
    boton_historia.pack(side="left", padx=5)

    boton_reglas = tk.Button(botones_historia_reglas, text="Mostrar Reglas", command=mostrar_reglas)
    boton_reglas.pack(side="left", padx=5)

    entrada_texto = tk.Entry(marco)
    entrada_texto.pack(pady=5)
    
    def bloquear_entrada(event):
        # Mientras se presionan los atajos, bloquea la entrada de texto.
        if event.char == event.keysym and event.keysym not in ("Return", "r", "R", "h", "H", "n", "N"):
            entrada_texto.config(state="normal")
        else:
            entrada_texto.config(state="disabled")

    def desbloquear_entrada(event):
        # Desbloquea la entrada de texto cuando se deja de presionar un atajo.
        entrada_texto.config(state="normal")

    # Configuración de los bortones.
    boton_adivinar = tk.Button(marco, text="Adivinar", command=lambda: enviar_numero(juego, raiz, entrada_texto, mensaje_etiqueta, resultado_etiqueta, ranking_tabla))
    boton_adivinar.pack(pady=5)

    boton_nueva_partida = tk.Button(marco, text="Nueva Partida", command=lambda: nueva_partida(juego, resultado_etiqueta, mensaje_etiqueta, ranking_tabla))
    boton_nueva_partida.pack(pady=5)

    mensaje_etiqueta = tk.Label(raiz, text="", fg="red", bg='lightblue')
    mensaje_etiqueta.pack()

    resultado_etiqueta = tk.Label(raiz, text="", bg='lightblue')
    resultado_etiqueta.pack()

    # Configuración de la tabla de ranking.
    ranking_tabla = ttk.Treeview(raiz, columns=("Intento", "Número", "Muertos", "Heridos"), show="headings", height=14)
    ranking_tabla.heading("Intento", text="#")
    ranking_tabla.heading("Número", text="Número")
    ranking_tabla.heading("Muertos", text="Muertos")
    ranking_tabla.heading("Heridos", text="Heridos")
    ranking_tabla.column("Intento", anchor="center", width=60)
    ranking_tabla.column("Número", anchor="center", width=80)
    ranking_tabla.column("Muertos", anchor="center", width=130)
    ranking_tabla.column("Heridos", anchor="center", width=130)
    ranking_tabla.pack()

    juego = Juego()

    # Configuración de los atajos.
    raiz.bind("<Return>", lambda event=None: boton_adivinar.invoke())
    raiz.bind("r", lambda event=None: boton_reglas.invoke())
    raiz.bind("R", lambda event=None: boton_reglas.invoke())
    raiz.bind("h", lambda event=None: boton_historia.invoke())
    raiz.bind("H", lambda event=None: boton_historia.invoke())
    raiz.bind("n", lambda event=None: boton_nueva_partida.invoke())
    raiz.bind("N", lambda event=None: boton_nueva_partida.invoke())

    raiz.bind("<Key>", bloquear_entrada)
    raiz.bind("<KeyRelease>", desbloquear_entrada)

    # Configuración de la ventana.
    raiz.resizable(width=False, height=False)

    menubar = tk.Menu(raiz)
    raiz.config(menu=menubar)
    
    juego_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Juego", menu=juego_menu)
    juego_menu.add_command(label="Guardar Registro de Partida", command=guardar_registro_partida)
    juego_menu.add_separator()
    juego_menu.add_command(label="Salir", command=raiz.quit)
    
if __name__ == "__main__":
    raiz = tk.Tk()
    crear_interfaz(raiz)
    raiz.mainloop()
