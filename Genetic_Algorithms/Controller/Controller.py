# IMPORTS

import View.MainWindow as VM
import View.FractalWindow as VF
import View.GenerationsWindow as VG
import Model.Fractal as MF
import Model.GeneticAlgorithm as MG
import Model.EnumValoresR as ME
import ntpath
import shutil
import os
from textwrap import wrap
import random


# CLASSES
class Controller:

    # Variables globales necesarias
    mainWindow = fractalWindow = generationsWindow = None
    archivoImagen = None
    cantidadGeneraciones = 10
    elementos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    algoritmo = None

    def __init__(self):
        '''
        Constructor
        '''

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
        """
        Function: Esta funcion es la encargada de validar que todos los datos obtenidos de la interfaz del algoritmo
        de fractales sean correctos
        Inputs:
        Outputs: Devuelve todos los paramteros para crear fractales
        """
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
        """
        Function: Esta funcion es la encargada de abrir la imagen y guardarla en una variable global
        Inputs:
        Outputs:
        """
        self.archivoImagen = VM.filedialog.askopenfile(
            title="Seleccione archivo", initialdir="../Siluetas/", filetypes=[("Archivos png", ".png")])
        try:
            self.mainWindow.mostrarNombreArchivo(ntpath.basename(self.archivoImagen.name))
            self.archivoImagen = self.archivoImagen.name
        except:
            return

    def algoritmoGenetico(self):
        """
        Function: Esta es la funcion principal del programa, encargada de ejecutar el algoritmo genetico que se
        encargara de utilizar todas las funciones(Crear fractales, Funcion fitness, Normalizar, Funcion de mutacion,
        Funcion de cruce, Sacar promedios, etc)
        Inputs:
        Outputs:
        """

        #Borramos los directorios de generaciones si existen
        self.borrarDirectoriosGeneraciones()

        # Creamos un nuevo algoritmo para aplicarle todas las funciones(fitness, genetica, mutaciones)
        self.algoritmo = MG.Algoritmo()

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

                        listaArboles.append(arbol)

                    primeraG = False

                # Crea las generaciones siguientes con valores de genetica
                else:

                    listaArbolesAnterior = self.algoritmo.listaDeGeneraciones[contadorGeneraciones - 1]

                    # Se modifican todos los arboles de la generacion anterior para agregar los porcentajes y cadenas de
                    # bits
                    for arbol in listaArbolesAnterior:
                        # Llamamos a la funcion fitness para obtener los porcentajes de similitud
                        arbol.porcentaje = self.algoritmo.fitness(self.archivoImagen, arbol.path)
                        sumaPorcentajes += arbol.porcentaje

                        # Llamamos la funcion que nos crea la cadena de bits
                        arbol.cadenaBits = self.crearCadenaBits(arbol)

                    # Obtiene la lista de los porcentajes de los arboles normalizados
                    listaNormalizacion = self.normalizar(sumaPorcentajes, listaArbolesAnterior)

                    # Obtiene la lista de supervivencia de los candidates
                    listaPorcentajesCandidatos = self.obtenerListaProbabilidad(self.elementos, listaNormalizacion)

                    # Se ejecutara 5 veces ya que ocupamos 5 parejas de arboles para generar 10 nuevos individuos
                    for i in range(5):
                        # Obtenemos las posiciones de los candidatos mas aptos para cruzarlos
                        num1, num2 = self.obtenerPosicionCandidatos(listaPorcentajesCandidatos)

                        # Obtenemos las cadenas de cromosomas de los dos nuevos arboles
                        cadenaBA1, cadenaBA2, mutacion1, mutacion2 = self.cruzarArbolesCandidatos(num1, num2,
                                                                                                  listaArbolesAnterior)

                        # Creamos el primer arbol nuevo
                        Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen = \
                            self.crearParametrosConBits(cadenaBA1)

                        arbolN1 = MF.Tree(Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen,
                                          False, contadorGeneraciones + 1, (i * 2) + 1)
                        # Agregamos si hubo mutacion
                        arbolN1.mutacion = mutacion1

                        # Agregamos los padres
                        arbolN1.padres.append(listaArbolesAnterior[num1])
                        arbolN1.padres.append(listaArbolesAnterior[num2])

                        listaArboles.append(arbolN1)

                        # Creamos el segundo arbol nuevo
                        Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen = \
                            self.crearParametrosConBits(cadenaBA2)

                        arbolN2 = None
                        if i == 0:
                            arbolN2 = MF.Tree(Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen,
                                              False, contadorGeneraciones + 1, 2)
                        else:
                            arbolN2 = MF.Tree(Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen,
                                              False, contadorGeneraciones + 1, (i * 2) + 2)

                        # Agregamos si hubo mutacion
                        arbolN2.mutacion = mutacion1

                        # Agregamos los padres
                        arbolN2.padres.append(listaArbolesAnterior[num1])
                        arbolN2.padres.append(listaArbolesAnterior[num2])
                        listaArboles.append(arbolN2)

                # Agregamos la generacion creada a la lista de generaciones
                self.algoritmo.listaDeGeneraciones.append(listaArboles)

            contadorGeneraciones += 1

        print("Terminó de procesar")

    def obtenerDivisores(self, cadena):
        """
        Function: Funcion encargada de obtener todos los divisores del numero total de caracteres de una cadena
        Inputs: Cadena de caracteres
        Outputs: Lista con todos los divisores
        """
        listaDivisores = []

        # Se hace de 1 hasta 8+1 porque el tamaño de un cromosoma es de 8 bits
        for i in range(1, 8 + 1):

            if len(cadena) % i == 0:
                listaDivisores.append(i)

        return listaDivisores

    def mutacion(self, cadena):
        """
        Function: Funcion encargada de hacer la mutacion respectiva a una cadena de bits
        Inputs: Cadena de caracteres
        Outputs: Cadena de caracteres mutada
        """

        # Obtenemos los divisores del tamaño de la cadena
        listaValoresPADividir = self.obtenerDivisores(cadena)
        cantidadWrap = random.choice(listaValoresPADividir)

        # Dividimos la cadena en conjuntos de bits
        listaCaracteres = wrap(cadena, cantidadWrap)

        # Obtenemos posicion random de la lista de conjuntos de bits
        posicionBitsAModificar = random.randint(0, len(listaCaracteres) - 1)

        # Obtenemos un conjunto o cadena de bits de la lista de conjuntos
        cadenaBits = listaCaracteres[posicionBitsAModificar]

        # Invertimos los caracters, si es 1 pasa a 0 y lo contrario
        cadenaNueva = ""
        for i in range(len(cadenaBits)):

            if cadenaBits[i] == '1':
                cadenaNueva += '0'
            else:
                cadenaNueva += '1'

        # Remplazamos el conjunto anterior de bits con el nuevo conjunto invertido
        listaCaracteres[posicionBitsAModificar] = cadenaNueva

        # Creamos la cadena final con todos los conjuntos ya modificados de la listaCaracteres
        cadenaFinal = ""
        for conjunto in listaCaracteres:
            cadenaFinal += conjunto

        return cadenaFinal

    def obtenerPosicionCandidatos(self, lista):
        """
        Function: Funcion encargada de obtener la posicion de dos arboles en una lista
        Inputs: Lista de arboles
        Outputs: Posiciones de 2 arboles
        """

        num1 = num2 = 0
        num1 = random.choice(lista)
        while True:

            num2 = random.choice(lista)
            if not num2 == num1:
                break

        return int(num1), int(num2)

    def cruzarArbolesCandidatos(self, num1, num2, lista):
        """
        Function: Funcion encargada de cruzar las cadenas de bits de 2 arboles de una lista de arboles
        Inputs: Posiciones de los dos arboles y la lista con los arboles
        Outputs: Cadenas de bits cruzadas de los 2 nuevos arboles y los valores de mutacion, si la tuvieron
        """

        # Obtenemos los dos arboles que se van a cruzar de la generacion anterior
        arbol1 = lista[num1]
        arbol2 = lista[num2]

        puntoCorte = random.randint(0, len(arbol1.cadenaBits) - 1)

        listaCadenas = [arbol1.cadenaBits[0:puntoCorte] +
                        arbol2.cadenaBits[puntoCorte + 1: len(arbol2.cadenaBits) - 1], arbol2.cadenaBits[0:puntoCorte] +
                        arbol1.cadenaBits[puntoCorte + 1: len(arbol1.cadenaBits) - 1]]

        # Proceso de mutacion
        mutacion = [False, True]
        pesos = [0.95, 0.05]
        listaProbabilidadMutacion = self.obtenerListaProbabilidad(mutacion, pesos)

        listaHayMutacion = []
        for i in range(2):
            hayMutacion = random.choice(listaProbabilidadMutacion)

            if hayMutacion:
                listaCadenas[i] = self.mutacion(listaCadenas[i])

            listaHayMutacion.append(hayMutacion)

        return listaCadenas[0], listaCadenas[1], listaHayMutacion[0], listaHayMutacion[1]

    def obtenerListaProbabilidad(self, elementos, pesos):
        """
        Function: Funcion encargada de generar la cantidad de números según su probabilidad y los guarda en una lista
        Inputs: Lista de elementos y la lista con los pesos
        Outputs: Lista con los pesos almacenados en proporcion segun su probabilidad de aparicion
        """

        lista = []  # Lista que almacena el resultado

        for e, p in zip(elementos, pesos):
            # se almacenan repetidos los elementos el número de veces según la probabilidad de aparicion elegida
            # por ejemplo si el 1 tiene 0.5 probabilidades de aparecer, entonces se guardará 50 veces
            lista += [e] * int(p * 100)

        return lista

    def normalizar(self, sumaPorcentajes, listaArboles):
        """
        Function: Funcion encargada de normalizar los porcentajes de cada arbol en la lista de arboles
        Inputs: Suma total de los porcentajes y la lista con los arboles
        Outputs: Lista con los valores normalizados
        """

        listaNormalizada = []
        for arbol in listaArboles:
            normalizacion = round((arbol.porcentaje / sumaPorcentajes), 2)
            arbol.normalizacion = normalizacion
            listaNormalizada.append(normalizacion)

        return listaNormalizada

    def crearParametrosRandom(self):
        """
        Function: Funcion encargada de generar los parametros random para crear la primera generacion de arboles a
        partir de un enumerable con valores predeterminados
        Inputs:
        Outputs: Parametros para crear un nuevo arbol fractal
        """

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

        # print("Depth: " + str(Depth))
        # print("Thickness: " + str(Thickness))
        # print("BranchThickness" + str(listaRangosP[0]))
        # print("BranchQuantity" + str(listaRangosP[1]))
        # print("ForkAngle" + str(listaRangosP[2]))
        # print("BaseLen" + str(listaRangosP[3]))

        return Depth, Thickness, listaRangosP[0], listaRangosP[1], listaRangosP[2], listaRangosP[3]

    def crearCadenaBits(self, arbol):
        """
        Function: Funcion encargada de generar la cadena de bits de todos los parametros de un arbol fractal
        Inputs: Arbol fractal
        Outputs: Cadena de bits de todos esos valores
        """

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
        """
        Function: Funcion encargada de generar los parametros de creacion de un arbol fractal a travez de una cadena de
        bits
        Inputs: Cadena de Bits
        Outputs: Parametros para crear arboles fractales
        """

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
        """
        Function: Funcion encargada de validar que el parametro generado a partir del cruce no sea mayor que el limite
        puesto de generacion de ese parametro
        Inputs: Parametro a validar y tupla con los valores predeterminados de ese parametro
        Outputs: Parametro modificado para que cumpla con los limites
        """

        parametro = int(parametro, 2)

        # Caso de que el parametro sea mayor que el limite
        if parametro > tupla[1]:
            parametro = tupla[1]

        # Caso de que el parametro sea menor que el limite
        if parametro < tupla[0]:
            parametro = tupla[0]

        return parametro

    def borrarDirectoriosGeneraciones(self):
        """
        Function: Funcion encargada de borrar todos los directorios de generaciones con el unico proposito de no tener
        que borrarlos manualmente cada que se corre el algoritmo
        Inputs:
        Outputs:
        """

        i = 0
        while i < self.cantidadGeneraciones:

            # Creamos el directorio de cada generacion
            path = "..\Generaciones\Generacion_" + str(i + 1)

            try:
                shutil.rmtree(path)

            except:
                print("Directorios no borrados")
                return
            i += 1

        print("Directorios borrados")
        return

    def main(self):
        '''
        Function: Funcion encargada de correr el programa fuente
        Inputs:
        Outputs:
        '''

        # Window Instance
        #self.mainWindow = VM.MainWindow(self)
        #self.mainWindow.main()
        self.generationsWindow = VG.GenerationsWindow(self, 10, [])
        self.generationsWindow.main()



# This is going to create a controller and call main function
if __name__ == '__main__':
    controller = Controller()
    controller.main()
