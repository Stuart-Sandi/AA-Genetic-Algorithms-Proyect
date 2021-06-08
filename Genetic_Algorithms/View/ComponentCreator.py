from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk


class ComponentCreator:

    PAD = 20
    WIDHTWINDOW = 860
    HEIGHTWINDOW = 350

    def createWindow(self, pTitle, pBackground, WIDHTWINDOW, HEIGHTWINDOW):
        '''
        Function: This function is responsible for creating a window with a title and the background color
        Inputs: Title, Background color
        Outputs: Window
        '''

        window = Tk()
        window.resizable(width=False, height=False)
        window.title(pTitle)

        # Window location = center of screen
        x_window = window.winfo_screenwidth() // 2 - WIDHTWINDOW // 2
        y_window = window.winfo_screenheight() // 2 - HEIGHTWINDOW // 2
        position = str(WIDHTWINDOW) + "x" + str(HEIGHTWINDOW) + "+" + str(x_window) + "+" + str(y_window)

        window.geometry(position)
        window.configure(background=pBackground)
        return window

    def createFrame(self, pComponent, pRow, pColumn, pWidth, pHeight):
        '''
        Function: This function is responsible for creating a frame
        Inputs: Frame Place, Row, Column, Width, Height
        Outputs: Frame
        '''
        frame = Frame(pComponent, width=pWidth, height=pHeight, highlightbackground='red', highlightthicknes=3)
        frame.grid(row=pRow, column=pColumn, padx=self.PAD, pady=self.PAD, ipadx=self.PAD, ipady=self.PAD)
        frame.grid_propagate(False)
        return frame

    def createLabel(self, pComponent, pText, pX, pY, pWidth, pHeight):
        '''
        Function: This function is responsible for creating a Label
        Inputs: Label Place, Label Text, X, Y, Width, Height
        Outputs: Label
        '''
        label = Label(pComponent, text=pText)
        label.configure(font=("Tahoma", 12, "italic"), relief='sunken', bd=5)
        label.place(x=pX, y=pY, width=pWidth, height=pHeight)
        return label

    def createEntry(self, pComponent, pX, pY, pWidth, pHeight):
        '''
        Function: This function is responsible for creating a Entry
        Inputs: Entry Place, X, Y, Width, Height
        Outputs: Entry
        '''
        entry = Entry(pComponent)
        entry.configure(font=("Tahoma", 10, "italic"), bd=5)
        entry.place(x=pX, y=pY, width=pWidth, height=pHeight)
        return entry

    def createScroll(self, pComponent, pOrient, pCommand, pX, pY, pWidth, pHeight):
        scroll = Scrollbar(pComponent, orient=pOrient, command=pCommand)
        if pOrient == HORIZONTAL:
            scroll.place(x=pX, y=pY, pWidth=pWidth)
        else:
            scroll.place(x=pX, y=pY, height=pHeight)
        return scroll

    def createText(self, pComponent, pX, pY, pWidth, pHeight):
        '''
        Function: This function is responsible for creating a TextArea
        Inputs: TextArea Place, X, Y, Width, Height
        Outputs: TextArea
        '''
        text = Text(pComponent)
        text.config(font=("Consolas", 10), bd=5)
        text.place(x=pX, y=pY, width=pWidth, height=pHeight)
        return text

    def createComboBox(self, pComponent, pX, pY, pWidth, pHeight):
        '''
        Function: This function is responsible for creating a ComboBox
        Inputs: ComboBox Place, X, Y, Width, Height
        Outputs: ComboBox
        '''
        combobox = Combobox(pComponent)
        combobox.place(x=pX, y=pY, width=pWidth, height=pHeight)
        return combobox

    def createButtons(self, pComponent, pText, pCommand, pX, pY, pWidth, pHeight):
        '''
        Function: This function is responsible for creating a Button
        Inputs: Button Place, Button Text, Function, X, Y, Width, Height
        Outputs: Button
        '''
        button = Button(pComponent, text=pText, command=pCommand)
        button.configure(font=("Tahoma", 10, "italic"), bd=5)
        button.place(x=pX, y=pY, width=pWidth, height=pHeight)
        return button

    def createBotonesArboles(self, pComponent, listaGeneraciones):

        matrizBotones = []
        for i in range(10):

            listaBotones = []
            for w in range(10):
                # Obtenemos la imagen del arbol
                img = PhotoImage(file="..\Silueta1.png")

                listaBotones.append(Button(pComponent, image=img, width=115, height=115).grid(row=i, column=w))

            matrizBotones.append(listaBotones)

        return matrizBotones

    def createCanvas(self, pComponent, cantidadGeneraciones):

        canvas = Canvas(pComponent, width=1180, height=450)
        scrollbar = Scrollbar(pComponent, orient="vertical", command=canvas.yview)
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
        self.createBotonesArboles(scrollable_frame, [])

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return canvas
