import cv2
import random
import Model.EnumValoresR as ME
from textwrap import wrap
from PIL import Image


class Algoritmo:
    listaDeGeneraciones = []

    def __init__(self):
        return

    @staticmethod
    def calcularAreaContorno(srcImg):
        """
        Function: Funcion encargada de calcular el area de un contorno en una imagen
        Inputs: Imagen
        Outputs: Area del contorno
        """
        src = srcImg
        imagen = cv2.imread(src)

        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        gris = cv2.GaussianBlur(gris, (7, 7), 3)

        _, binaria = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_TRIANGLE)

        contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # dibujar los contornos
        imgFinal = cv2.imread("../Images/Blanco.png")
        cv2.drawContours(imgFinal, contornos, -1, (0, 0, 0), 3)

        area = 0
        for c in contornos:
            area = cv2.contourArea(c)

        path = (srcImg[:-4]) + "_Contorno.png"
        cv2.imwrite(path, imgFinal)
        return area

    @staticmethod
    def calcularSimilitudPixeles(srcImg1, srcImg2):
        """
        Function: Funcion encargada de calcular un porcentaje de similitud entre 2 imagenes
        Inputs: Imagenes a comparar
        Outputs: Procentaje
        """
        im = Image.open(srcImg1)
        pixels = list(im.getdata())

        im2 = Image.open(srcImg2)
        pixels2 = list(im2.getdata())

        # Cuenta los pixeles negros de la img1
        contadorPixeles = 0
        for i in range(len(pixels)):

            if not pixels[i] == (255, 255, 255):
                contadorPixeles += 1

        # Cuenta los pixeles negros iguales de la img1 y img2
        contador = 0
        rango = 5
        for i in range(len(pixels)):

            # if pixels[i] == pixels2[i] and pixels[i] != (255, 255, 255):
            #    contador += 1

            for j in range(rango):

                if pixels[i] != (255, 255, 255):
                    # Izquierda
                    if i - j >= 0:

                        if pixels[i] == pixels2[i - j]:
                            # match
                            contador += 1
                            break

                    # Derecha
                    if i + j <= 360000:

                        if pixels[i] == pixels2[i + j]:
                            # match
                            contador += 1
                            break

                    # Arriba
                    if i - (600 * j) >= 0:

                        if pixels[i] == pixels2[i - (j * 600)]:
                            # match
                            contador += 1
                            break

                    # Abajo
                    if i + (600 * j) <= 360000:

                        if pixels[i] == pixels2[i + (j * 600)]:
                            # match
                            contador += 1
                            break
                else:
                    break

        # Porcentaje de similitud
        return (contador / contadorPixeles) * 100

    def fitness(self, srcImg1, srcImg2):
        """
        Function: Funcion encargada de devolver el porcentaje dde similitud entre dos imagenes teniendo en cuenta la
        cantidad de pixeles iguales y el area de las dos figuras
        Inputs: Imagenes
        Outputs: Porcentaje de similitud
        """

        areaImg1 = self.calcularAreaContorno(srcImg1)
        areaImg2 = self.calcularAreaContorno(srcImg2)

        porcentajeArea = 0

        # Se calcula la similitud de las areas del contorno de las dos imagenes
        if areaImg1 >= areaImg2:
            porcentajeArea = 100 - ((areaImg1 - areaImg2) * 100) / areaImg1
        else:
            porcentajeArea = 100 - ((areaImg2 - areaImg1) * 100) / areaImg2

        porcentajeSimilitudPixeles = self.calcularSimilitudPixeles(srcImg1, srcImg2)

        return round(((porcentajeArea + porcentajeSimilitudPixeles) / 2), 4)

    @staticmethod
    def obtenerPosicionCandidatos(lista):
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

        listaCadenas = [arbol1.cadenaBits[0:puntoCorte] + arbol2.cadenaBits[puntoCorte: len(arbol2.cadenaBits)],
                        arbol2.cadenaBits[0:puntoCorte] + arbol1.cadenaBits[puntoCorte: len(arbol1.cadenaBits)]]

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

        return listaCadenas[0], listaCadenas[1], listaHayMutacion[0], listaHayMutacion[1], puntoCorte

    @staticmethod
    def obtenerListaProbabilidad(elementos, pesos):
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

    @staticmethod
    def normalizar(sumaPorcentajes, listaArboles):
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

    @staticmethod
    def crearParametrosRandom():
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

    @staticmethod
    def obtenerDivisores(cadena):
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

    @staticmethod
    def crearCadenaBits(arbol):
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
                     BaseLen1 + BaseLen2 + ForkAngle1 + ForkAngle2

        return cadenaBits

    def crearParametrosConBits(self, cadenaBits):
        """
        Function: Funcion encargada de generar los parametros de creacion de un arbol fractal a travez de una cadena de
        bits
        Inputs: Cadena de Bits
        Outputs: Parametros para crear arboles fractales
        """

        # Hace un wrap para separar los bits en cadenas de 8 bits
        Depth, Thickness, BranchThickness1, BranchThickness2, BranchQuantity1, BranchQuantity2, BaseLen1, BaseLen2, \
        ForkAngle1, ForkAngle2 = wrap(cadenaBits, 8)

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

    @staticmethod
    def validarRangoParametrosBits(parametro, tupla):
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
