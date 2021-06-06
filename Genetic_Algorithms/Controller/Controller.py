# IMPORTS

import View.MainWindow as VM
import View.FractalWindow as VF
import Model.Fractal as MF
import Model.GeneticAlgorithm as MG
import Model.EnumValoresR as ME
import ntpath
import os
from textwrap import wrap
import random


# CLASSES
class Controller:
    mainWindow = fractalWindow = None
    archivoImagen = None
    cantidadGeneraciones = 10
    elementos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

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
            self.archivoImagen = self.archivoImagen.name
        except:
            return

    def algoritmoGenetico(self):

        # Creamos un nuevo algoritmo para aplicarle todas las funciones(fitness, genetica, mutaciones)
        algoritmo = MG.Algoritmo()

        contadorGeneraciones = 0
        primeraG = True

        # Ejecuta el while hasta que termine la cantidad de generaciones
        while contadorGeneraciones < self.cantidadGeneraciones:

            # Creamos el directorio de cada generacion
            path = "..\Generaciones\Generacion_" + str(contadorGeneraciones + 1)
            if not os.path.exists(path):
                os.mkdir(path)

                sumaPorcentajes = 0
                listaArboles = []
                listaNormalizacion = []
                listaPorcentajesCandidatos = []

                # Crea la primera generacion con valores random
                if primeraG:

                    # Creamos 10 arboles
                    for i in range(10):
                        # Las siguientes variables hacen referencia a los parametros de:
                        # Depth, Thickness, branch_thickness, branch_quantity, fork_angle, base_len
                        de, th, br_th, br_qu, f_a, b_l = self.crearParametrosRandom()
                        arbol = MF.Tree(de, th, br_th, br_qu, f_a, b_l, False, contadorGeneraciones + 1, i + 1)

                        # Llamamos a la funcion fitness para obtener los porcentajes de similitud
                        arbol.porcentaje = algoritmo.fitness(self.archivoImagen, arbol.path)
                        sumaPorcentajes += arbol.porcentaje

                        # Llamamos la funcion que nos crea la cadena de bits
                        arbol.cadenaBits = self.crearCadenaBits(arbol)
                        # print(arbol.cadenaBits+"\n")

                        listaArboles.append(arbol)

                    primeraG = False

                # Crea las generaciones siguientes con valores de genetica
                else:

                    for i in range(10):
                        listaArboles = algoritmo.listaDeGeneraciones[contadorGeneraciones-1]
                        #Vamos por esta parte


                # Obtiene la lista de los porcentajes de los arboles normalizados
                listaNormalizacion = self.normalizar(sumaPorcentajes, listaArboles)

                listaPorcentajesCandidatos = self.obtenerListaProbabilidad(self.elementos, listaNormalizacion)

                algoritmo.listaDeGeneraciones.append(listaArboles)

            contadorGeneraciones += 1

    # Funcion que genera la cantidad de números según su probabilidad y los guarda en una lista
    def obtenerListaProbabilidad(self, elementos, pesos):
        lista = []  # Lista que almacena el resultado

        for e, p in zip(elementos, pesos):
            # se almacenan repetidos los elementos el número de veces según la probabilidad de aparicion elegida
            # por ejemplo si el 1 tiene 0.5 probabilidades de aparecer, entonces se guardará 50 veces
            lista += [e] * int(p * 100)

        return lista

    def normalizar(self, sumaPorcentajes, listaArboles):

        listaNormalizada = []
        for arbol in listaArboles:
            normalizacion = arbol.porcentaje / sumaPorcentajes
            arbol.normalizacion = normalizacion
            listaNormalizada.append(normalizacion)

        return listaNormalizada

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

        print("Depth: " + str(Depth))
        print("Thickness: " + str(Thickness))
        print("BranchThickness" + str(listaRangosP[0]))
        print("BranchQuantity" + str(listaRangosP[1]))
        print("ForkAngle" + str(listaRangosP[2]))
        print("BaseLen" + str(listaRangosP[3]))

        return Depth, Thickness, listaRangosP[0], listaRangosP[1], listaRangosP[2], listaRangosP[3]

    def crearCadenaBits(self, arbol):

        cadenaBits = ""
        Depth = format(arbol.depth, "08b")
        Thickness = format(arbol.thickness, "08b")
        BranchThickness1 = format(arbol.branch_thickness[0], "08b")
        BranchThickness2 = format(arbol.branch_thickness[1], "08b")
        BranchQuantity1 = format(arbol.branch_quantity[0], "08b")
        BranchQuantity2 = format(arbol.branch_quantity[1], "08b")
        ForkAngle1 = format(int(arbol.fork_angle[0]), "08b")
        ForkAngle2 = format(int(arbol.fork_angle[1]), "08b")
        BaseLen1 = format(arbol.base_len[0], "08b")
        BaseLen2 = format(arbol.base_len[1], "08b")
        cadenaBits = Depth + Thickness + BranchThickness1 + BranchThickness2 + BranchQuantity1 + BranchQuantity2 + \
                     ForkAngle1 + ForkAngle2 + BaseLen1 + BaseLen2

        return cadenaBits

    def crearParametrosConBits(self, cadenaBits):

        # Hace un wrap para separar los bits en cadenas de 8 bits
        Depth, Thickness, BranchThickness1, BranchThickness2, BranchQuantity1, BranchQuantity2, ForkAngle1, ForkAngle2 \
            , BaseLen1, BaseLen2 = wrap(cadenaBits, 8)

        # Convierte los numeros a enteros y valida que el numero no supere los limites
        Depth = self.validarRangoParametrosBits(Depth, ME.ValoresRandom.Depth.value)
        Thickness = self.validarRangoParametrosBits(Thickness, ME.ValoresRandom.Thickness.value)
        BranchThickness1 = self.validarRangoParametrosBits(BranchThickness1, ME.ValoresRandom.BranchThickness.value)
        BranchThickness2 = self.validarRangoParametrosBits(BranchThickness2, ME.ValoresRandom.BranchThickness.value)
        BranchQuantity1 = self.validarRangoParametrosBits(BranchQuantity1, ME.ValoresRandom.BranchQuantity.value)
        BranchQuantity2 = self.validarRangoParametrosBits(BranchQuantity2, ME.ValoresRandom.BranchQuantity.value)
        ForkAngle1 = self.validarRangoParametrosBits(ForkAngle1, ME.ValoresRandom.ForkAngle.value)
        ForkAngle2 = self.validarRangoParametrosBits(ForkAngle2, ME.ValoresRandom.ForkAngle.value)
        BaseLen1 = self.validarRangoParametrosBits(BaseLen1, ME.ValoresRandom.BaseLen.value)
        BaseLen2 = self.validarRangoParametrosBits(BaseLen2, ME.ValoresRandom.BaseLen.value)

        # Crea las tuplasde los rangos y las ordena de menor a mayor
        BranchThickness = sorted((BranchThickness1, BranchThickness2))
        BranchQuantity = sorted((BranchQuantity1, BranchQuantity2))
        ForkAngle = sorted((float(ForkAngle1), float(ForkAngle2)))
        BaseLen = sorted((BaseLen1, BaseLen2))

        return Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen

    def validarRangoParametrosBits(self, parametro, tupla):

        parametro = int(parametro, 2)

        # Caso de que el parametro sea mayor que el limite
        if parametro > tupla[1]:
            parametro = tupla[1]

        # Caso de que el parametro sea menor que el limite
        if parametro < tupla[0]:
            parametro = tupla[0]

        return parametro

    def main(self):
        '''
        Function: This function is going to create a Window with all its characteristics
        Inputs:
        Outputs:
        '''

        self.mainWindow.main()


# This is going to create a controller and call main function
if __name__ == '__main__':
    controller = Controller()
    controller.main()
