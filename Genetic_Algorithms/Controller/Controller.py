# IMPORTS

import View.MainWindow as VM
import View.FractalWindow as VF
import Model.Fractal as MF
import Model.GeneticAlgorithm as MG
import Model.EnumValoresR as ME
import ntpath
import os
import random


# CLASSES
class Controller:
    mainWindow = fractalWindow = None
    archivoImagen = None
    cantidadGeneraciones = 10

    def __init__(self):
        '''
        Constructor
        '''

        # Window Instance
        self.mainWindow = VM.MainWindow(self)

    def probarAlgoFractales(self):
        """
        Function: This function is going show fractal algorithm
        Inputs:
        Outputs:
        """

        self.fractalWindow = VF.FractalWindow(self)
        self.fractalWindow.main()

        return

    def fractales(self):
        """
        Function: This function is going to create a fractal with some parameters
        Inputs:
        Outputs:
        """

        depth, thickness, branch_thickness, fork_angle, branch_quantity, base_len = self.validarDatosFractales()
        if depth != -1:
            MF.Tree(depth, thickness, branch_thickness, fork_angle, branch_quantity, base_len, True, 0, 0)
        else:
            self.fractalWindow.showMessagesBox("¡Faltan valores o valores incorrectos!")
            self.fractalWindow.window.destroy()
            self.fractalWindow = VF.FractalWindow(self)
            self.fractalWindow.main()
        return

    def validarDatosFractales(self):
        w = self.fractalWindow

        # OBTIENE LOS DATOS DE LA PANTALLA
        depth = w.comboBoxDepth.get()
        thickness = w.comboBoxThickness.get()
        branch_thickness = w.entryBranchT.get()
        fork_angle = w.entryForkAngle.get()
        branch_quantity = w.entryBranchQ.get()
        base_len = w.entryBaseLen.get()

        # VALIDA QUE NO SEAN NULOS
        if depth != "" and \
                thickness != "" and \
                branch_thickness != "" and \
                fork_angle != "" and \
                branch_quantity != "" and \
                base_len != "":

            try:
                depth = int(depth)
                thickness = int(thickness)

                tmp = branch_thickness.split(",")
                branch_thickness = (int(tmp[0]), int(tmp[1]))

                tmp = fork_angle.split(",")
                fork_angle = (float(tmp[0]), float(tmp[1]))

                tmp = branch_quantity.split(",")
                branch_quantity = (int(tmp[0]), int(tmp[1]))

                tmp = base_len.split(",")
                base_len = (int(tmp[0]), int(tmp[1]))

                return depth, thickness, branch_thickness, fork_angle, branch_quantity, base_len

            except:
                return -1, 0, 0, 0, 0, 0

        return -1, 0, 0, 0, 0, 0

    def abrirImagen(self):
        self.archivoImagen = VM.filedialog.askopenfile(
            title="Seleccione archivo", initialdir="../Siluetas/", filetypes=[("Archivos png", ".png")])
        try:
            self.mainWindow.mostrarNombreArchivo(ntpath.basename(self.archivoImagen.name))
        except:
            return

    def algoritmoGenetico(self):

        # Creamos un nuevo algoritmo para aplicarle todas las funciones(fitness, genetica, mutaciones)
        algoritmo = MG.Algoritmo()

        contadorGeneraciones = 1

        # Ejecuta el while hasta que termine la cantidad de generaciones
        while contadorGeneraciones <= self.cantidadGeneraciones:

            # Creamos el directorio de cada generacion
            path = "..\Generaciones\Generacion_"+str(contadorGeneraciones)
            if not os.path.exists(path):
                os.mkdir(path)

                listaArboles = []
                #Creamos 10 arboles
                for i in range(10):

                    # Las siguientes variables hacen referencia a los parametros de:
                    # Depth, Thickness, branch_thickness, branch_quantity, fork_angle, base_len
                    de, th, br_th, br_qu, f_a, b_l = self.crearParametrosRandom()
                    arbol = MF.Tree(de, th, br_th, br_qu, f_a, b_l, False, contadorGeneraciones, i+1)
                    listaArboles.append(arbol)

                algoritmo.listaDeGeneraciones.append(listaArboles)

            contadorGeneraciones += 1
        print("Termino el algoritmo")
        # print(algoritmo.fitness("../ImagenPrueba1.png", "../ImagenPrueba3.png"))

    def crearParametrosRandom(self):

        listaValoresP = []
        for parametro in ME.ValoresRandom:
            listaValoresP.append(parametro.value)

        Depth = random.randint(listaValoresP[0][0], listaValoresP[0][1])
        Thickness = random.randint(listaValoresP[1][0], listaValoresP[1][1])

        listaRangosP = []
        for i in range(2, len(listaValoresP)):

            num1 = random.randint(listaValoresP[i][0], listaValoresP[i][1])
            num2 = random.randint(listaValoresP[i][0], listaValoresP[i][1])

            if num1 >= num2:
                listaRangosP.append((num2, num1))
            else:
                listaRangosP.append((num1, num2))

        #print("Depth: " + str(Depth))
        #print("Thickness: " + str(Thickness))
        #print("BranchThickness" + str(listaRangosP[0]))
        #print("BranchQuantity" + str(listaRangosP[1]))
        #print("ForkAngle" + str(listaRangosP[2]))
        #print("BaseLen" + str(listaRangosP[3]))

        return Depth, Thickness, listaRangosP[0], listaRangosP[1], listaRangosP[2], listaRangosP[3]

    def main(self):
        '''
        Function: This function is going to create a Window with all its characteristics
        Inputs:
        Outputs:
        '''

        self.mainWindow.main()
        #self.crearParametrosRandom()


# This is going to create a controller and call main function
if __name__ == '__main__':
    controller = Controller()
    controller.main()
