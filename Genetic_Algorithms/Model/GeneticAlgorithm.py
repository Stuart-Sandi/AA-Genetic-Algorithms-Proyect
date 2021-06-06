import cv2
import numpy as np
from PIL import Image


class Algoritmo:

    listaDeGeneraciones = []

    def __init__(self):
        print()

    def calcularAreaContorno(self, srcImg):
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

        for c in contornos:
            area = cv2.contourArea(c)

        path = (srcImg[:-4])+"_Contorno.png"
        cv2.imwrite(path, imgFinal)
        return area

    # Porcentaje de similitud entre dos imagenes
    def calcularSimilitudPixeles(self, srcImg1, srcImg2):
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

            #if pixels[i] == pixels2[i] and pixels[i] != (255, 255, 255):
            #    contador += 1

            for j in range(rango):

                if pixels[i] != (255, 255, 255):
                    # Izquierda
                    if i - j >= 0:

                        if pixels[i] == pixels2[i-j]:
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

        areaImg1 = self.calcularAreaContorno(srcImg1)
        areaImg2 = self.calcularAreaContorno(srcImg2)

        porcentajeArea = 0

        # Se calcula la similitud de las areas del contorno de las dos imagenes
        if areaImg1 >= areaImg2:
            porcentajeArea = 100 - ((areaImg1 - areaImg2) * 100) / areaImg1
        else:
            porcentajeArea = 100 - ((areaImg2 - areaImg1) * 100) / areaImg2

        porcentajeSimilitudPixeles = self.calcularSimilitudPixeles(srcImg1, srcImg2)

        return (porcentajeArea + porcentajeSimilitudPixeles) / 2
