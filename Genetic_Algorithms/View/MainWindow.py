# IMPORTS
from tkinter import messagebox

from View.ComponentCreator import ComponentCreator


# CLASSES
class MainWindow:
    PAD = 20
    WIDHTWINDOW = 860
    HEIGHTWINDOW = 650

    # Component Creator
    comCreator = ComponentCreator()

    # Componentes de la ventana
    window = None

    def __init__(self, controller):
        '''
            Constructor
        '''

        self.controller = controller
        self.window = self.comCreator.createWindow('Algoritmos Genéticos', 'white')
        frame = self.comCreator.createFrame(self.window, 0, 0, self.WIDHTWINDOW-80, self.HEIGHTWINDOW-80)

        #LABELS
        self.comCreator.createLabel(frame, "ALGORITMOS GENÉTICOS", 300, 20, 220, 70)
        self.comCreator.createLabel(frame, "Generación de arboles fractales: ", 40, 150, 300, 40)

        #BUTTONS
        self.comCreator.createButtons(frame, "Probar algoritmo", self.controller.probarAlgoFractales, 360, 150, 140, 40)

    def showMessagesBox(self, dato):
        messagebox.showerror("Error", dato)

    def main(self):
        self.window.mainloop()
