# IMPORTS
import ntpath
import this
from functools import partial
from tkinter import *

from PIL import Image, ImageTk

from View.ComponentCreator import ComponentCreator


# CLASSES
class GenerationsWindow:
    PAD = 20
    WIDHTWINDOW = 1300
    HEIGHTWINDOW = 550

    # Component Creator
    comCreator = ComponentCreator()

    # Componentes de la ventana
    window = frame = canvas = None

    # Lista con las imagenes
    imagenes = []

    # Matriz de botones
    mBotones = None

    def __init__(self, controller, cantidadGeneraciones, listaGeneraciones):
        '''
            Constructor
        '''

        self.controller = controller
        self.window = self.comCreator.createWindow('Algoritmos Genéticos/Generaciones de la 1 a la ' +
                                                   str(cantidadGeneraciones), 'white', self.WIDHTWINDOW,
                                                   self.HEIGHTWINDOW, 0)
        self.frame = self.comCreator.createFrame(self.window, 0, 0, self.WIDHTWINDOW - 80, self.HEIGHTWINDOW - 80)
        self.canvas = self.createCanvas(listaGeneraciones)

    def main(self):
        self.window.mainloop()

    def createCanvas(self, listaGeneraciones):

        canvas = Canvas(self.frame, width=1180, height=450)
        scrollbar = Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Crea la matriz de botones con la imagen de los arboles
        self.createBotonesArboles(scrollable_frame, listaGeneraciones)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return canvas

    def createBotonesArboles(self, pComponent, listaGeneraciones):

        self.mBotones = []
        for i in range(len(listaGeneraciones)):

            listaBotones = []
            for w in range(len(listaGeneraciones[i])):
                # Nombre del arbol
                nombre = listaGeneraciones[i][w].nombre

                # Obtenemos la imagen del arbol
                img = Image.open(listaGeneraciones[i][w].path)
                img = img.resize((115, 80), Image.ANTIALIAS)  # Redimension (Alto, Ancho)
                img = ImageTk.PhotoImage(img)
                self.imagenes.append(img)
                button = Button(pComponent, image=img, text=nombre, width=115, height=115, compound="top")
                button.configure(command=partial(self.controller.datosBoton, (i, w)))
                button.grid(row=i, column=w)
                listaBotones.append(button)

            self.mBotones.append(listaBotones)

        return
