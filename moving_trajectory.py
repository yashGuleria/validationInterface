"""This script contains functions to generate and draw the aircraft trajectories on the SCREEN"""


import numpy as np
import pandas as pd
from buttons import Button
import os
import datetime
import pygame
WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 3
fpsClock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
DARKGREEN = (0, 128, 0)
DARK_GREEN = (100, 210, 150)
LIGHT_BLUE = (224, 255, 255)
PASTEL_BLUE = (202, 228, 241)
MAP = pygame.image.load('map.jpg')
sector = pygame.transform.scale(MAP, (WIDTH-100, HEIGHT-100))


def to_pixels(lon, lat):
    """convert lon lat to pixels. Returns integer values of x,y as pixels"""
    map = [103.8, 107.8, 2, 5]  # x1,x2,y1,y2
    x_diff = lon - map[0]
    y_diff = lat - map[2]

    xrange = map[1] - map[0]
    yrange = map[3] - map[2]

    return int(x_diff/xrange * (1749-72) + 72), int(954 - (y_diff/yrange) * (954-26))


def pred_trajectory(filename, color):
    action = True
    df = pd.read_csv(filename)
    lon1 = []
    lat1 = []
    for i in range(len(df)):
        pixels = to_pixels(df.loc[i, 'longitude'], df.loc[i, 'latitude'])
        pygame.draw.circle(SCREEN, color, (pixels[0], pixels[1]), 4)
        # pygame.display.update()
    return action


Damog = [4.206944444444445, 105.0038888888889]

damog_trans = to_pixels(Damog[1], Damog[0])
print(damog_trans)

accept = Button(82, 1000, 'Accept')
reject = Button(550, 1000, 'Reject')
next_scen = Button(1020, 1000, 'Next')
exitbutton = Button(1570, 1000, 'Exit')


def line_evolve(resf, unresf, color1, color2):

    action = True
    resflight = pd.read_csv(resf)
    unresflight = pd.read_csv(unresf)

    if pd.to_datetime(resflight.loc[0, 'time']) > pd.to_datetime(unresflight.loc[0, 'time']):
        startfirst = unresflight
        startsecond = resflight
        delta = pd.to_timedelta(
            startsecond.loc[0, 'time']) - pd.to_timedelta(startfirst.loc[0, 'time'])
        delta_str_minutes = int(str(delta)[10:12])
        delta_str_seconds = int(str(delta)[13:])
        offset = int((delta_str_minutes*60 + delta_str_seconds)/5)
    else:
        startfirst = resflight
        startsecond = unresflight
        delta = pd.to_timedelta(
            startsecond.loc[0, 'time']) - pd.to_timedelta(startfirst.loc[0, 'time'])
        delta_str_minutes = int(str(delta)[10:12])
        delta_str_seconds = int(str(delta)[13:])
        offset = int((delta_str_minutes*60 + delta_str_seconds)/5)

    for i in range(len(resflight)):
        # print(i)
        # SCREEN.fill(WHITE)
        SCREEN.blit(sector, (0, 0))
        # making the predicted trajectory
        trajp = pred_trajectory('1_3K40.csv', LIGHT_BLUE)

        if i < offset:
            pixels = to_pixels(
                startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
            pygame.draw.circle(SCREEN, color1, (pixels[0], pixels[1]), 3)

            fpsClock.tick(FPS)
            for event in pygame.event.get():
                continue
            # if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)

            # keys = pygame.key.get_pressed()

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

            exitinterface = exitbutton.draw_button(SCREEN)
            if exitinterface == True:
                pygame.quit()
            pygame.display.update()
        else:
            pixels1 = to_pixels(
                startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
            pygame.draw.circle(SCREEN, color1, (pixels1[0], pixels1[1]), 3)
            pixels2 = to_pixels(
                startsecond.loc[i-offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])
            pygame.draw.circle(SCREEN, color2, (pixels2[0], pixels2[1]), 3)
            fpsClock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                continue
            # keys = pygame.key.get_pressed()
            pygame.draw.circle(
                SCREEN, RED, (damog_trans[0], damog_trans[1]), 5)

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

            exitinterface = exitbutton.draw_button(SCREEN)
            if exitinterface == True:
                pygame.quit()

            pygame.display.update()

    return action
