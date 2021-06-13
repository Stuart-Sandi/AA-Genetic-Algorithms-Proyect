# IMPORTS

import View.MainWindow as VM
import View.FractalWindow as VF
import View.GenerationsWindow as VG
import View.FractalInfoWindow as VFI
import Model.Fractal as MF
import Model.GeneticAlgorithm as MG
import shutil
import os


# CLASSES
class Controller:
    # Variables globales necesarias
    mainWindow = fractalWindow = generationsWindow = fractalInfoWindow = None
    archivoImagen = None
    cantidadGeneraciones = None
    elementos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    algoritmo = None

    def __init__(self):
        """
        Constructor
        """

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
            self.mainWindow.mostrarNombreArchivo(self.archivoImagen.name)
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
        try:
            if self.mainWindow.entry.get() != "":
                self.cantidadGeneraciones = int(self.mainWindow.entry.get())
            else:
                self.mainWindow.showMessagesBox("¡Debe ingresar la cantidad de generaciones a realizar!")
                return
        except:
            self.mainWindow.showMessagesBox("¡Debe ingresar un numero en las generaciones a realizar!")
            return

        # Borramos los directorios de generaciones si existen
        self.borrarDirectoriosGeneraciones()

        # Creamos un nuevo algoritmo para aplicarle todas las funciones(fitness, genetica, mutaciones)
        self.algoritmo = None
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
                        de, th, br_th, br_qu, f_a, b_l = self.algoritmo.crearParametrosRandom()
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
                        arbol.cadenaBits = self.algoritmo.crearCadenaBits(arbol)

                    # Obtiene la lista de los porcentajes de los arboles normalizados
                    listaNormalizacion = self.algoritmo.normalizar(sumaPorcentajes, listaArbolesAnterior)

                    # Obtiene la lista de supervivencia de los candidates
                    listaPorcentajesCandidatos = self.algoritmo.obtenerListaProbabilidad(
                        self.elementos, listaNormalizacion)

                    # Se ejecutara 5 veces ya que ocupamos 5 parejas de arboles para generar 10 nuevos individuos
                    for i in range(5):
                        # Obtenemos las posiciones de los candidatos mas aptos para cruzarlos
                        num1, num2 = self.algoritmo.obtenerPosicionCandidatos(listaPorcentajesCandidatos)

                        # Obtenemos las cadenas de cromosomas de los dos nuevos arboles
                        cadenaBA1, cadenaBA2, mutacion1, mutacion2, puntoCorte = self.algoritmo.cruzarArbolesCandidatos(
                            num1, num2,
                            listaArbolesAnterior)

                        # Creamos el primer arbol nuevo
                        Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen = \
                            self.algoritmo.crearParametrosConBits(cadenaBA1)

                        arbolN1 = MF.Tree(Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen,
                                          False, contadorGeneraciones + 1, (i * 2) + 1)
                        # Agregamos si hubo mutacion
                        arbolN1.mutacion = mutacion1
                        if arbolN1.mutacion:
                            print("Hubo mutacion en el arbol: "+arbolN1.nombre)

                        # Agregamos el punto de corte
                        arbolN1.puntoCorte = puntoCorte - 1

                        # Agregamos los padres
                        arbolN1.padres = [listaArbolesAnterior[num1], listaArbolesAnterior[num2]]

                        listaArboles.append(arbolN1)

                        # Creamos el segundo arbol nuevo
                        Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen = \
                            self.algoritmo.crearParametrosConBits(cadenaBA2)

                        arbolN2 = None
                        if i == 0:
                            arbolN2 = MF.Tree(Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen,
                                              False, contadorGeneraciones + 1, 2)
                        else:
                            arbolN2 = MF.Tree(Depth, Thickness, BranchThickness, BranchQuantity, ForkAngle, BaseLen,
                                              False, contadorGeneraciones + 1, (i * 2) + 2)

                        # Agregamos si hubo mutacion
                        arbolN2.mutacion = mutacion2
                        if arbolN2.mutacion:
                            print("Hubo mutacion en el arbol: "+arbolN2.nombre)

                        # Agregamos el punto de corte
                        arbolN2.puntoCorte = puntoCorte - 1

                        # Agregamos los padres
                        arbolN2.padres = [listaArbolesAnterior[num1], listaArbolesAnterior[num2]]

                        listaArboles.append(arbolN2)

                # Agregamos la generacion creada a la lista de generaciones
                self.algoritmo.listaDeGeneraciones.append(listaArboles)

            contadorGeneraciones += 1

        # Agrega la cadena de cromosomas a la ultima generacion
        listaArbolesAnterior = self.algoritmo.listaDeGeneraciones[len(self.algoritmo.listaDeGeneraciones) - 1]

        # Se modifican todos los arboles de la generacion anterior para agregar los porcentajes y cadenas de
        # bits
        for arbol in listaArbolesAnterior:
            # Llamamos la funcion que nos crea la cadena de bits
            arbol.cadenaBits = self.algoritmo.crearCadenaBits(arbol)

        print("Terminó de procesar")
        self.generationsWindow = None
        self.generationsWindow = VG.GenerationsWindow(self, len(self.algoritmo.listaDeGeneraciones),
                                                      self.algoritmo.listaDeGeneraciones)
        self.generationsWindow.main()

    def borrarDirectoriosGeneraciones(self):
        """
        Function: Funcion encargada de borrar todos los directorios de generaciones con el unico proposito de no tener
        que borrarlos manualmente cada que se corre el algoritmo
        Inputs:
        Outputs:
        """

        i = 0
        while i < self.cantidadGeneraciones:

            try:
                # Creamos el directorio de cada generacion
                path = "..\Generaciones\Generacion_" + str(i + 1)
                shutil.rmtree(path)

            except:
                print("Directorios no borrados")
                return
            i += 1

        print("Directorios borrados")
        return

    def datosBoton(self, button):

        arbol = self.algoritmo.listaDeGeneraciones[button[0]][button[1]]
        self.fractalInfoWindow = VFI.FractalInfoWindow(self, arbol)
        self.fractalInfoWindow.main()

    def main(self):
        """
        Function: Funcion encargada de correr el programa fuente
        Inputs:
        Outputs:
        """

        # Window Instance
        self.mainWindow = VM.MainWindow(self)
        self.mainWindow.main()


# This is going to create a controller and call main function
if __name__ == '__main__':
    controller = Controller()
    controller.main()
