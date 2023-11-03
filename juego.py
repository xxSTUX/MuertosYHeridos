import random
import time

class Juego:
    def __init__(self):
        # Inicializa una nueva instancia.
        self.reiniciar_juego()

    def reiniciar_juego(self):
        # Reinicia el juego, generando un nuevo número secreto y limpiando los intentos previos.
        self.numero_secreto = self.generar_numero()
        self.intentos_anteriores = []
        self.limite = 0
        self.intentos = []

    def generar_numero(self):
        # Genera un número secreto de 4 cifras al azar.
        # Returns:
        #     str: Número secreto generado.
        numeros = list(range(10))
        random.shuffle(numeros)
        numero_secreto = ''.join(map(str, numeros[:4]))
        return numero_secreto

    def calcular_muertos(self, cifras):
        # Calcula el número de "muertos" en una suposición.
        # Args:
        #     cifras (str): Suposición del jugador.
        # Returns:
        #     int: Número de muertos.
        muertos = 0
        for i in range(4):
            if self.numero_secreto[i] == cifras[i]:
                muertos += 1
        return muertos

    def calcular_heridos(self, cifras):
        # Calcula el número de "heridos" en una suposición.
        # Args:
        #     cifras (str): Suposición del jugador.
        # Returns:
        #     int: Número de heridos.
        heridos = 0
        for i in range(4):
            if self.numero_secreto[i] != cifras[i] and self.numero_secreto[i] in cifras:
                heridos += 1
        return heridos

    def jugar(self, entrada, mensaje_etiqueta, resultado_etiqueta, ranking_tabla, raiz):
        # Realiza un intento en el juego y actualiza la interfaz con los resultados.
        # Args:
        #     entrada (str): Suposición del jugador.
        #     mensaje_etiqueta (tk.Label): Etiqueta para mensajes de error.
        #     resultado_etiqueta (tk.Label): Etiqueta para mostrar los resultados.
        #     ranking_tabla (ttk.Treeview): Tabla para mostrar el ranking.
        #     raiz (tk.Tk): Ventana principal de la aplicación.

        mensaje_etiqueta.config(text="")
        if len(entrada) != 4:
            mensaje_etiqueta.config(text="Por favor, introduzca un número de 4 cifras.")
            return
        elif entrada in self.intentos_anteriores:
            mensaje_etiqueta.config(text="Ya has intentado este número. Elige uno diferente.")
            return
        elif not entrada.isdigit():
            mensaje_etiqueta.config(text="Sólo se permiten números.")
        else:
            cifras = list(entrada)
            if len(set(cifras)) != 4:
                mensaje_etiqueta.config(text="Por favor, no repita cifras en su número.")
                return
            else:
                self.intentos_anteriores.append(entrada)

        self.limite += 1
        muertos = self.calcular_muertos(cifras)
        heridos = self.calcular_heridos(cifras)
        resultado_etiqueta.config(text=f"Muertos: {muertos}, Heridos: {heridos}")

        self.intentos.append((self.limite, entrada, muertos, heridos))
        self.actualizar_ranking(ranking_tabla)

        if muertos == 4:
            tiempo_fin = time.time()
            resultado_etiqueta.config(text=f"¡Felicidades! Adivinaste el número secreto con {self.limite} intentos.")
            self.intentos.append((self.limite, tiempo_fin, entrada, muertos, heridos))
            self.actualizar_ranking(ranking_tabla)
            return

        if self.limite == 14:
            mensaje_etiqueta.config(text="Sobrepasaste el límite de intentos. Inicia nueva partida.")
            raiz.update()
            return self.reiniciar_juego()

    def actualizar_ranking(self, ranking_tabla):
        # Actualiza la tabla de ranking en la interfaz.
        # Args:
        #     ranking_tabla (ttk.Treeview): Tabla para mostrar el ranking.

        intentos_ordenados = sorted(self.intentos, key=lambda x: (x[0], x[1]))
        ranking_tabla.delete(*ranking_tabla.get_children())
        for intento in intentos_ordenados:
            ranking_tabla.insert("", "end", values=(intento[0], intento[1], intento[2], intento[3]))
