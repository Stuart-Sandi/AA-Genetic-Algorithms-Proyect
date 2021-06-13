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
    WIDHTWINDOW = 700
    HEIGHTWINDOW = 500

    # Component Creator
    comCreator = ComponentCreator()

    # Componentes de la ventana
    window = None
    entry = None
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

        # LABELS
        self.comCreator.createLabel(frame, "ALGORITMOS GENÉTICOS", 220, 20, 220, 70)
        self.comCreator.createLabel(frame, "Generación de arboles fractales: ", 40, 130, 310, 40)
        self.comCreator.createLabel(frame, "Algoritmo Genetico: ", 40, 200, 200, 40)
        self.lblNombreArchivo = self.comCreator.createLabel(frame, "", 40, 260, 125, 125)
        self.comCreator.createLabel(frame, "Cantidad de Generaciones:", 180, 260, 220, 40)

        # ENTRY
        self.entry = self.comCreator.createEntry(frame, 180, 300, 220, 40)

        # BUTTONS
        self.comCreator.createButtons(frame, "Probar algoritmo", self.controller.probarAlgoFractales, 360, 129, 150, 40)
        self.comCreator.createButtons(frame, "Abrir Imagen",self.controller.abrirImagen, 39, 400, 125, 40)
        self.buttonAGenetic = self.comCreator.createButtons(frame, "Ejecutar Algoritmo", self.controller.algoritmoGenetico,
                                                            180, 400, 150, 40)
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
