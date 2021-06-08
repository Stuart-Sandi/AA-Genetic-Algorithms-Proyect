# IMPORTS
import tkinter as tk
from tkinter import ttk
from View.ComponentCreator import ComponentCreator


# CLASSES
class GenerationsWindow:
    PAD = 20
    WIDHTWINDOW = 1300
    HEIGHTWINDOW = 550

    # Component Creator
    comCreator = ComponentCreator()

    # Componentes de la ventana
    window = None

    def __init__(self, controller, cantidadGeneraciones, listaGeneraciones):
        '''
            Constructor
        '''

        self.controller = controller
        self.window = self.comCreator.createWindow('Algoritmos Genéticos/Generaciones de la 1 a la '+
                                                   str(cantidadGeneraciones), 'white', self.WIDHTWINDOW,
                                                   self.HEIGHTWINDOW)
        frame = self.comCreator.createFrame(self.window, 0, 0, self.WIDHTWINDOW - 80, self.HEIGHTWINDOW - 80)
        canvas = self.comCreator.createCanvas(frame, cantidadGeneraciones)

    def main(self):
        self.window.mainloop()

# import tkinter as tk
# from tkinter import ttk
#
# root = tk.Tk()
# container = ttk.Frame(root)
# canvas = tk.Canvas(container)
# scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
# scrollable_frame = ttk.Frame(canvas)
#
# scrollable_frame.bind(
#     "<Configure>",
#     lambda e: canvas.configure(
#         scrollregion=canvas.bbox("all")
#     )
# )
#
# canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#
# canvas.configure(yscrollcommand=scrollbar.set)
#
# for i in range(50):
#     ttk.Label(scrollable_frame, text="Sample scrolling label").pack()
#
# container.pack()
# canvas.pack(side="left", fill="both", expand=True)
# scrollbar.pack(side="right", fill="y")
#
# root.mainloop()
