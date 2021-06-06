# IMPORTS
from tkinter import messagebox

from View.ComponentCreator import ComponentCreator


# CLASSES
class FractalWindow:
    PAD = 20
    WIDHTWINDOW = 860
    HEIGHTWINDOW = 650

    # Component Creator
    comCreator = ComponentCreator()

    # Componentes de la ventana
    window = None
    entryBranchT = entryForkAngle = entryBranchQ = entryBaseLen = None
    comboBoxDepth = comboBoxThickness = None

    def __init__(self, controller):
        '''
            Constructor
        '''

        self.controller = controller
        self.window = self.comCreator.createWindow('Algoritmos Genéticos/Fractales', 'white', self.WIDHTWINDOW, self.HEIGHTWINDOW)
        frame = self.comCreator.createFrame(self.window, 0, 0, self.WIDHTWINDOW-80, self.HEIGHTWINDOW-80)

        #LABELS
        self.comCreator.createLabel(frame, "ALGORITMO DE FRACTALES", 290, 20, 230, 70)
        self.comCreator.createLabel(frame, "Seleccione la profundidad del árbol: ", 120, 140, 280, 40)
        self.comCreator.createLabel(frame, "Seleccione el grosor del tronco: ", 150, 200, 250, 40)
        self.comCreator.createLabel(frame, "Seleccione el rango de grosor de las ramas: ", 70, 250, 330, 40)
        self.comCreator.createLabel(frame, "Seleccione el rango de los ángulos entre ramas: ", 40, 300, 360, 40)
        self.comCreator.createLabel(frame, "Seleccione el rango de la cantidad de ramas: ", 50, 350, 350, 40)
        self.comCreator.createLabel(frame, "Seleccione el rango de largo de las ramas: ", 70, 400, 330, 40)

        #ENTRY
        self.entryBranchT = self.comCreator.createEntry(frame, 430, 250, 140, 40)
        self.entryForkAngle = self.comCreator.createEntry(frame, 430, 300, 140, 40)
        self.entryBranchQ = self.comCreator.createEntry(frame, 430, 350, 140, 40)
        self.entryBaseLen = self.comCreator.createEntry(frame, 430, 400, 140, 40)

        #COMBOBOX
        self.comboBoxDepth = self.comCreator.createComboBox(frame, 430, 140, 140, 40)
        self.comboBoxDepth["values"] = ["5", "6", "7", "8"]
        self.comboBoxThickness = self.comCreator.createComboBox(frame, 430, 200, 140, 40)
        self.comboBoxThickness["values"] = ["5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]

        #BUTTONS
        self.comCreator.createButtons(frame, "Ejecutar", self.controller.fractales, 360, 500, 100, 40)

    def showMessagesBox(self, dato):
        messagebox.showerror("Error", dato)

    def main(self):
        self.window.mainloop()