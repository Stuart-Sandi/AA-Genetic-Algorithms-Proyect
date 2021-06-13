# IMPORTS
import ntpath
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

from View.ComponentCreator import ComponentCreator


# CLASSES
class MainWindow:
    PAD = 20
    WIDHTWINDOW = 860
    HEIGHTWINDOW = 450

    # Component Creator
    comCreator = ComponentCreator()

    # Componentes de la ventana
    window = None
    lblNombreArchivo = None
    buttonAGenetic = None
    imagen = None

    def __init__(self, controller):
        '''
            Constructor
        '''

        self.controller = controller
        self.window = self.comCreator.createWindow('Algoritmos Genéticos', 'white', self.WIDHTWINDOW, self.HEIGHTWINDOW, 1)
        frame = self.comCreator.createFrame(self.window, 0, 0, self.WIDHTWINDOW-80, self.HEIGHTWINDOW-80)

        #LABELS
        self.comCreator.createLabel(frame, "ALGORITMOS GENÉTICOS", 300, 20, 220, 70)
        self.comCreator.createLabel(frame, "Generación de arboles fractales: ", 40, 150, 310, 40)
        self.comCreator.createLabel(frame, "Algoritmo Genetico: ", 40, 300, 200, 40)
        self.lblNombreArchivo = self.comCreator.createLabel(frame, "", 300, 250, 125, 125)

        #BUTTONS
        self.comCreator.createButtons(frame, "Probar algoritmo", self.controller.probarAlgoFractales, 600, 149, 150, 40)
        self.comCreator.createButtons(frame, "Abrir Imagen",self.controller.abrirImagen, 470, 299, 100, 40)
        self.buttonAGenetic = self.comCreator.createButtons(frame, "Ejecutar Algoritmo", self.controller.algoritmoGenetico,
                                                            600, 299, 150, 40)
        self.buttonAGenetic['state'] = tkinter.DISABLED

    def showMessagesBox(self, dato):
        messagebox.showerror("Error", dato)

    def mostrarNombreArchivo(self, path):
        img = Image.open(path)
        img = img.resize((125, 125), Image.ANTIALIAS)  # Redimension (Alto, Ancho)
        self.imagen = ImageTk.PhotoImage(img)
        self.lblNombreArchivo.configure(image=self.imagen)
        self.buttonAGenetic.configure(state=tkinter.NORMAL)
        #self.buttonAGenetic['state'] = tkinter.NORMAL

    def main(self):
        self.window.mainloop()
