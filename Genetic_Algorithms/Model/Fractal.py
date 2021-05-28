import math
import pygame


class Tree:

    window = None
    screen = None

    def __init__(self):

        pygame.init()
        self.window = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Fractal Tree")
        self.screen = pygame.display.get_surface()

        self.drawTree(300, 550, -90, 7, 2, 20.0, 10.0)
        pygame.display.flip()
        while True:
            self.input(pygame.event.wait())

    def drawTree(self, x1, y1, angle, depth, branch_thickness, fork_angle, base_len):
        if depth > 0:
            x2 = x1 + int(math.cos(math.radians(angle)) * depth * base_len)
            y2 = y1 + int(math.sin(math.radians(angle)) * depth * base_len)

            pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), branch_thickness)

            # Ramificaciones derecha
            i = 2
            while i != 0:
                self.drawTree(x2, y2, angle + (fork_angle * i), depth - 1, branch_thickness, fork_angle, base_len)
                i -= 1

            #ramificaciones Izquierda
            i = 1
            while i != 0:
                self.drawTree(x2, y2, angle - (fork_angle * i), depth - 1, branch_thickness, fork_angle, base_len)
                i -= 1

    def input(self, event):
        if event.type == pygame.QUIT:
            exit(0)
