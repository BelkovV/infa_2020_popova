import pygame
from pygame.draw import *
from numpy import sin, cos, pi

def hemicircle(screen, color, x, y, r, sign=1, precise=100):
    a = [(int(x+r*cos(t/precise)), int(y-sign*r*sin(t/precise))) for t in range(0, int(precise*pi))]
    polygon(screen, color, a)


def heart(screen, color, x, y, r, phi = pi/4):
    hemicircle(screen, color, x, y, int(r), -1)
    hemicircle(screen, color, x-int(r/2), y, int(r/2))
    hemicircle(screen, color, x+int(r/2), y, int(r/2))
    a = (int(x - r*cos(phi)), int(y + r*sin(phi)))
    b = (int(x + r*cos(phi)), int(y + r*sin(phi)))
    c = (x, int(y + r/sin(phi)))
    polygon(screen, color, [a, b, c])

if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    screen.fill((0, 0, 0))
    heart(screen, (255, 0, 0), 150, 150, 50, pi/4)
    pygame.display.update()
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            clock.tick(20)
    pygame.quit()
