import math
import pygame
import random


class Tree:

    window = None
    screen = None
    x1 = 300
    y1 = 550
    angle = -90
    mostrarFractal = None

    # Parametros de entrada
    depth = None
    thickness = None
    branch_thickness = None
    fork_angle = None
    branch_quantity = None
    base_len = None

    def __init__(self, depth, thickness, branch_thickness, branch_quantity, fork_angle, base_len, mostrarFractal,
                 generacion, numArbol):

        #Guardamos los valores de los parametros
        self.depth = depth
        self.thickness = thickness
        self.branch_thickness = branch_thickness
        self.fork_angle = fork_angle
        self.branch_quantity = branch_quantity
        self.base_len = base_len
        self.mostrarFractal = mostrarFractal

        # Crea el display que mostrara el fractal
        pygame.init()
        self.window = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Fractal Tree")
        self.screen = pygame.display.get_surface()
        self.screen.fill([255, 255, 255])

        # Llama a la funcion creadora del fractal
        self.drawTree(self.x1, self.y1, self.angle, self.depth, self.branch_thickness, self.fork_angle, self.base_len,
                      self.branch_quantity, self.thickness)

        if self.mostrarFractal:
            pygame.display.flip()

            # SE MANTIENE ESPERANDO POR CERRAR EL DISPLAY
            while True:
                if self.input(pygame.event.wait()) == 1:
                    break

        else:
            path = "..\Generaciones\Generacion_"+str(generacion)+"\Arbol_"+str(numArbol)+".png"
            pygame.image.save(self.screen, path)

        # CIERRA LA EJECUCION DEL DISPLAY DE PYGAME
        pygame.display.quit()

    def drawTree(self, x1, y1, angle, depth, branch_thickness, fork_angle, base_len, branch_quantity, thickness):
        if depth > 0:
            base_len_random = random.randint(base_len[0], base_len[1])
            x2 = x1 + int(math.cos(math.radians(angle)) * depth * base_len_random)
            y2 = y1 + int(math.sin(math.radians(angle)) * depth * base_len_random)

            # Grosor del arbol
            thickness2 = thickness
            if thickness2 < 0:
                thickness2 = 0

            while thickness2 != -1:
                branch_thickness_random = random.randint(branch_thickness[0], branch_thickness[1])
                pygame.draw.line(self.screen, (0, 0, 0), (x1 - thickness2, y1), (x2 - thickness2, y2),
                                 branch_thickness_random)
                pygame.draw.line(self.screen, (0, 0, 0), (x1 + thickness2, y1), (x2 + thickness2, y2),
                                 branch_thickness_random)
                thickness2 -= 1

            # Cantidad de ramas random
            i = random.randint(branch_quantity[0], branch_quantity[1])

            # Si la cantidad de ramas es impar
            if not i % 2 == 0:
                self.drawTree(x2, y2, angle, depth - 1, branch_thickness, fork_angle,
                              base_len, branch_quantity, thickness - 2)
                # Le resta la iteracion ya hecha
                i -= 1

            if i != 1:

                # Lo divide entre 2 ya que hace 2 operaciones al mismo tiempo
                i = i / 2

                # Crea las ramificaciones tanto de la izquierda como de la derecha
                while i > 0:
                    fork_angle_random = random.randint(fork_angle[0], fork_angle[1])
                    self.drawTree(x2, y2, angle + (fork_angle_random * i), depth - 1, branch_thickness, fork_angle,
                                  base_len, branch_quantity, thickness - 2)
                    self.drawTree(x2, y2, angle - (fork_angle_random * i), depth - 1, branch_thickness, fork_angle,
                                  base_len, branch_quantity, thickness - 2)
                    i -= 1

    @staticmethod
    def input(event):
        if event.type == pygame.QUIT:
            return 1
        return 0

    def parametrosABinario(self):
        return
