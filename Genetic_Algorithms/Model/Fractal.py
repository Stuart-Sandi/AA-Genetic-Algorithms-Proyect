import math
import pygame
import random


class Tree:

    window = None
    screen = None

    def __init__(self):

        pygame.init()
        self.window = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Fractal Tree")
        self.screen = pygame.display.get_surface()

        x1 = 300
        x2 = 550
        angle = -90
        depth = 5
        branch_thickness = (1, 2)
        fork_angle = (20.0, 30.0)
        branch_quantity = (1, 3)
        base_len = (10.0, 15.0)

        self.drawTree(x1, x2, angle, depth, branch_thickness, fork_angle, base_len, branch_quantity)
        pygame.display.flip()
        while True:
            self.input(pygame.event.wait())

    def drawTree(self, x1, y1, angle, depth, branch_thickness, fork_angle, base_len, branch_quantity):
        if depth > 0:
            base_len_random = random.randint(base_len[0], base_len[1])
            x2 = x1 + int(math.cos(math.radians(angle)) * depth * base_len_random)
            y2 = y1 + int(math.sin(math.radians(angle)) * depth * base_len_random)

            branch_thickness_random = random.randint(branch_thickness[0], branch_thickness[1])
            pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), branch_thickness_random)

            # Ramificaciones derecha
            i = random.randint(branch_quantity[0], branch_quantity[1])
            while i != 0:
                fork_angle_random = random.randint(fork_angle[0], fork_angle[1])
                self.drawTree(x2, y2, angle + (fork_angle_random * i), depth - 1, branch_thickness, fork_angle, base_len, branch_quantity)
                i -= 1

            #ramificaciones Izquierda
            i = random.randint(branch_quantity[0], branch_quantity[1])
            while i != 0:
                fork_angle_random = random.randint(fork_angle[0], fork_angle[1])
                self.drawTree(x2, y2, angle - (fork_angle_random * i), depth - 1, branch_thickness, fork_angle, base_len, branch_quantity)
                i -= 1

    def input(self, event):
        if event.type == pygame.QUIT:
            exit(0)
