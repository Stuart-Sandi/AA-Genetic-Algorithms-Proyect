# IMPORTS
from tkinter import *
from PIL import Image, ImageTk

from View.ComponentCreator import ComponentCreator


# CLASSES
class FractalInfoWindow:
    PAD = 20
    WIDHTWINDOW = 700
    HEIGHTWINDOW = 650

    # Component Creator
    comCreator = ComponentCreator()

    # Componentes de la ventana
    window = None

    # Referencia al arbol
    arbol =  None
    imagen = None

    def __init__(self, controller, arbol):
        '''
            Constructor
        '''
        self.arbol = arbol
        self.controller = controller
        self.window = self.comCreator.createWindow(self.arbol.nombre, 'white', self.WIDHTWINDOW, self.HEIGHTWINDOW, 0)
        frame = self.comCreator.createFrame(self.window, 0, 0, self.WIDHTWINDOW-80, self.HEIGHTWINDOW-80)

        # Imagen del arbol en lbl
        img = Image.open(arbol.path)
        img = img.resize((150, 150), Image.ANTIALIAS)  # Redimension (Alto, Ancho)
        self.imagen = ImageTk.PhotoImage(img)
        lblImagen = self.comCreator.createLabel(frame, "", 225, 20, 200, 200)
        lblImagen.configure(image=self.imagen)

        # Propiedades del arbol
        self.comCreator.createLabel(frame, "Propiedades del arbol", 225, 240, 200, 40)

        mutacion = self.arbol.mutacion
        if mutacion:
            mutacion = "Si"
        else:
            mutacion = "No"

        padres = self.arbol.padres
        if padres is None:
            padres = "No tiene"
        else:
            padres = str(self.arbol.padres[1].nombre)+", "+str(self.arbol.padres[0].nombre)

        porcentajeA = self.arbol.normalizacion
        if porcentajeA is None:
            porcentajeA = '-'
        else:
            porcentajeA = str(self.arbol.normalizacion)

        label = Label(frame, text=
                        "Nombre: "+str(self.arbol.nombre)+"\n"+
                        "Arbol: #"+str(self.arbol.numArbol)+"\n"+
                        "Generacion: "+str(self.arbol.generacion)+"\n\n"+
                        "Profundidad: "+str(self.arbol.depth)+"\n"+
                        "Grosor del tronco: "+str(self.arbol.thickness)+"\n"+
                        "Rango grosor de las ramas: "+str(self.arbol.branch_thickness)+"\n"+
                        "Rango cantidad de ramas: "+str(self.arbol.branch_quantity)+"\n"+
                        "Rango largo de las ramas: "+str(self.arbol.base_len)+"\n"+
                        "Rango ángulo de inclinacion: "+str(self.arbol.fork_angle)+"\n\n"+
                        "Padres: "+padres+"\n\n"+
                        "Sufrió Mutacion: "+mutacion+"\n"+
                        "Resultado Adaptabilidad: "+porcentajeA+"\n\n"
                        "Cadena de cromosomas: - Punto de corte: "+str(self.arbol.puntoCorte)
                        )
        label.configure(font=("Tahoma", 9, "italic"))
        label.place(x=20, y=300, width=600, height=250)

        entry = Entry(frame)
        entry.insert(0, str(self.arbol.cadenaBits))
        entry.place(x=20, y=555, width=600, height=40)
        # +str(self.arbol.cadenaBits)



    def main(self):
        self.window.mainloop()