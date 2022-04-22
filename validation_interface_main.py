from unicodedata import name
import pygame
from pygame.locals import *
# from buttons_copy import Button
from buttons import Button

import numpy as np
import pandas as pd
# from moving_trajectory import *
# from moving_trajectory_copy2 import *
from plotting_test import *
import sys

pygame.init()

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ATC VALIDATION ON AIR TRAFFIC CONFLICT RESOLUTION")

FPS = 3
fpsClock = pygame.time.Clock()
# color for the GUI
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
DARKGREEN = (0, 128, 0)
DARK_GREEN = (100, 210, 150)
LIGHT_BLUE = (224, 255, 255)
PASTEL_BLUE = (202, 228, 241)

font = pygame.font.SysFont('Arial', 25)
MAP = pygame.image.load('map.jpg')
sector = pygame.transform.scale(MAP, (WIDTH-350, HEIGHT-150))
rect = MAP.get_rect()
rect = rect.move(WIDTH, HEIGHT)


def to_pixels(lon, lat):
    """convert lon lat to pixels. Returns integer values of x,y as pixels"""
    map = [103.8, 107.8, 2, 5]  # x1,x2,y1,y2
    x_diff = lon - map[0]
    y_diff = lat - map[2]

    xrange = map[1] - map[0]
    yrange = map[3] - map[2]

    return int(x_diff/xrange * (1508-62) + 62), int(906 - (y_diff/yrange) * (906-24))


Damog = [4.206944444444445, 105.0038888888889]
damog_trans = to_pixels(Damog[1], Damog[0])
print(damog_trans)

resultlist = []

dir_res = 'resolved_initial/'
dir_unres = 'unres_initial'
sorted_resdir = sorted(os.listdir(
    dir_res), key=lambda x: int(x.split('.')[0][15:]))

sorted_unresdir = sorted(os.listdir(dir_unres),
                         key=lambda x: int(x.split('.')[0][15:]))
sorted_preddir = sorted(os.listdir(dir_pred),
                        key=lambda x: int(x.split('.')[0][15:]))


# main loop
running = True

while running:

    SCREEN.fill(PASTEL_BLUE)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
        SCREEN.blit(sector, (0, 0))

        if event.type == MOUSEBUTTONDOWN:
            # continue
            mx, my = pygame.mouse.get_pos()
            # print(mx, my)

        pygame.display.update()
        pygame.draw.circle(SCREEN, RED, (damog_trans[0], damog_trans[1]), 5)

        accepted = accept.draw_button(SCREEN)
        if accepted == True:
            print('Accpet pressed')
            # fpsClock.tick(FPS)

        rejected = reject.draw_button(SCREEN)
        if rejected == True:
            print('Rejected')

        nextclicked = next_scen.draw_button(SCREEN)
        if nextclicked == True:
            print('NEXT')

        viz = line_evolve(sorted_resdir, sorted_unresdir,
                          sorted_preddir, RED, BLACK)

        pygame.display.update()

pygame.quit()
