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

        self.drawTree(300, 550, -90, 10)
        pygame.display.flip()
        while True:
            self.input(pygame.event.wait())

    def drawTree(self, x1, y1, angle, depth):
        fork_angle = 20
        base_len = 10.0
        if depth > 0:
            x2 = x1 + int(math.cos(math.radians(angle)) * depth * base_len)
            y2 = y1 + int(math.sin(math.radians(angle)) * depth * base_len)
            pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
            self.drawTree(x2, y2, angle - fork_angle, depth - 1)
            self.drawTree(x2, y2, angle + fork_angle, depth - 1)

    def input(self, event):
        if event.type == pygame.QUIT:
            exit(0)
