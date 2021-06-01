import math
import pygame
import random


class Tree:
    window = None
    screen = None
    x1 = 300
    y1 = 550
    angle = -90

    def __init__(self):

        pygame.init()
        self.window = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Fractal Tree")
        self.screen = pygame.display.get_surface()
        self.screen.fill([255, 255, 255])

        depth = 8
        thickness = 5
        branch_thickness = (2, 3)
        fork_angle = (20.0, 30.0)
        branch_quantity = (2, 4)
        base_len = (10.0, 15.0)

        self.drawTree(self.x1, self.y1, self.angle, depth, branch_thickness, fork_angle, base_len, branch_quantity, thickness)
        pygame.display.flip()
        pygame.image.save(self.screen, "..\Imagen2.png")
        while True:
            self.input(pygame.event.wait())

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
                #Le resta la iteracion ya hecha
                i -= 1

            if i != 1:

                #Lo divide entre 2 ya que hace 2 operaciones al mismo tiempo
                i = i/2

                # Crea las ramificaciones tanto de la izquierda como de la derecha
                while i > 0:
                    fork_angle_random = random.randint(fork_angle[0], fork_angle[1])
                    self.drawTree(x2, y2, angle + (fork_angle_random * i), depth - 1, branch_thickness, fork_angle,
                                  base_len , branch_quantity, thickness - 2)
                    self.drawTree(x2, y2, angle - (fork_angle_random * i), depth - 1, branch_thickness, fork_angle,
                                  base_len , branch_quantity, thickness - 2)
                    i -= 1

    def input(self, event):
        if event.type == pygame.QUIT:
            exit(0)
