# IMPORTS
from tkinter import *

# CLASSES
class Window:
    PAD = 20
    WIDHTWINDOW = 860
    HEIGHTWINDOW = 650

    # Componentes de la ventana
    window = None

    def __init__(self, controller):
        '''
            Constructor
        '''

        self.controller = controller
        self.window = self.createWindow('Genetic Algorithms', 'white')

    def createWindow(self, pTitle, pBackground):
        '''
        Function: This function is responsible for creating a window with a title and the background color
        Inputs: Title, Background color
        Outputs: Window
        '''

        window = Tk()
        window.resizable(width=False, height=False)
        window.title(pTitle)

        # Window location = center of screen
        x_window = window.winfo_screenwidth() // 2 - self.WIDHTWINDOW // 2
        y_window = window.winfo_screenheight() // 2 - self.HEIGHTWINDOW // 2
        position = str(self.WIDHTWINDOW) + "x" + str(self.HEIGHTWINDOW) + "+" + str(x_window) + "+" + str(y_window)

        window.geometry(position)
        window.configure(background=pBackground)
        return window

    def main(self):
        self.window.mainloop()