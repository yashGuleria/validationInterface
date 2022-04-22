import numpy as np
import pandas as pd
import os
import sys
from buttons import Button, InfoButton
import datetime
import pygame
WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 10
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
sector = pygame.transform.scale(MAP, (WIDTH-350, HEIGHT-150))


def to_pixels(lon, lat):
    """convert lon lat to pixels. Returns integer values of x,y as pixels"""
    map = [103.8, 107.8, 2, 5]  # x1,x2,y1,y2
    x_diff = lon - map[0]
    y_diff = lat - map[2]

    xrange = map[1] - map[0]
    yrange = map[3] - map[2]

    return int(x_diff/xrange * (1508-62) + 62), int(906 - (y_diff/yrange) * (906-24))


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

accept = Button(82, 1000, 'ACCEPT')
reject = Button(550, 1000, 'REJECT')
next_scen = Button(1020, 1000, 'NEXT')
exitbutton = Button(1570, 1000, 'EXIT')

dir_res = 'resolved_initial/'
dir_unres = 'unres_initial/'
dir_pred = 'predicted_trajs/'

sorted_resdir = sorted(os.listdir(
    dir_res), key=lambda x: int(x.split('.')[0][15:]))
sorted_unresdir = sorted(os.listdir(dir_unres),
                         key=lambda x: int(x.split('.')[0][15:]))
sorted_preddir = sorted(os.listdir(dir_pred),
                        key=lambda x: int(x.split('.')[0][15:]))


def trimmed_flights(resflight, unresflight, pred_res):
    lengthlist = [len(resflight), len(unresflight), len(pred_res)]
    resflight_t = resflight.iloc[:min(lengthlist)]
    unresflight_t = unresflight.iloc[:min(lengthlist)]
    pred_res_t = pred_res.iloc[:min(lengthlist)]
    return resflight_t, unresflight_t, pred_res_t


def show_info(featurefile, index):
    """show information of the maneuvers"""
    action = True
    x = 1600
    y = 150
    delta = 50
    "show info of heading , CTD and merging waypoint"
    guideline1 = InfoButton(
        x+50, y-150, 'Please select a preference')
    guide1 = guideline1.draw_button(SCREEN)
    guideline2 = InfoButton(
        x+50, y-100, 'before maneuver initiation')
    guide2 = guideline2.draw_button(SCREEN)
    heading = InfoButton(x, y + 2*delta, 'Heading : ' +
                         str(featurefile.loc[index, 'headingAngle']) + chr(176))
    head = heading.draw_button(SCREEN)
    crosstrackdev = InfoButton(
        x, y + 3*delta, 'CTD : ' + str(featurefile.loc[index, 'crosstrack_dist_max']) + 'Nm')
    ctd = crosstrackdev.draw_button(SCREEN)
    pygame.display.update()

    return action


def segmentplot(df, index1, index2):
    action = True
    RED = (255, 0, 0)
    for _i in range(index1, index2+1):
        coord = to_pixels(df.loc[_i, 'longitude'], df.loc[_i, 'latitude'])
        pygame.draw.circle(SCREEN, RED, (coord[0], coord[1]), 3)
        pygame.display.update()
        fpsClock.tick(FPS)
    return action

    