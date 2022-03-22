"""This script contains functions to generate and draw the aircraft trajectories on the SCREEN"""


import numpy as np
import pandas as pd
from buttons import Button, InfoButton
# from buttons_copy import Button, InfoButton

import os

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

accept = Button(82, 1000, 'Accept')
reject = Button(550, 1000, 'Reject')
next_scen = Button(1020, 1000, 'Next')
exitbutton = Button(1570, 1000, 'Exit')

dir_res = 'resolved_initial/'
dir_unres = 'unres_initial/'
dir_pred = 'predicted_trajs/'

sorted_resdir = sorted(os.listdir(
    dir_res), key=lambda x: int(x.split('.')[0][15:]))
sorted_unresdir = sorted(os.listdir(dir_unres),
                         key=lambda x: int(x.split('.')[0][15:]))
sorted_preddir = sorted(os.listdir(dir_pred),
                        key=lambda x: int(x.split('.')[0][15:]))


def show_info(featurefile, index):
    action = True
    x = 1550
    y = 150
    delta = 50
    "show info of heading , CTD and merging waypoint"
    heading = InfoButton(x, y, 'Heading' +
                         str(featurefile.loc[index, 'headingAngle']))
    head = heading.draw_button(SCREEN)
    crosstrackdev = InfoButton(
        x, y + 2*delta, 'CTD' + str(featurefile.loc[index, 'crosstrack_dist_max']))
    ctd = crosstrackdev.draw_button(SCREEN)
    pygame.display.update()

    return action


def line_evolve(sorted_resdir, sorted_unresdir, sorted_preddir, color1, color2):
    action = True

    featurefile = pd.read_csv('featurefile_110222set1.csv')

    for index, (_d1, _d2, _d3) in enumerate(zip(sorted_resdir, sorted_unresdir, sorted_preddir)):
        resflight = pd.read_csv(dir_res + '{}'.format(_d1))
        unresflight = pd.read_csv(dir_unres + '{}'.format(_d2))
        pred_res = pd.read_csv(dir_pred + '{}'.format(_d3))
        print(_d1, _d2, _d3)
        # draw maneuver information

        # pygame.display.update()

        # calculating timesteps to maneuver initiation
        for f in range(len(featurefile)):
            if _d1 == featurefile.loc[f, 'resolvedflight']:
                maneuv_time = featurefile.loc[f, 'timetoresolution']
                steps = int((maneuv_time * 60) / 5)
                print(' maneuver initiation steps:  ', steps)
                break

        if len(resflight) > len(unresflight):
            shorterflight = unresflight

            if pd.to_datetime(resflight.loc[0, 'time']) > pd.to_datetime(unresflight.loc[0, 'time']):
                startfirst = unresflight
                startsecond = resflight
                delta = pd.to_timedelta(
                    startsecond.loc[0, 'time']) - pd.to_timedelta(startfirst.loc[0, 'time'])
                delta_str_minutes = int(str(delta)[10:12])
                delta_str_seconds = int(str(delta)[13:])
                offset = int((delta_str_minutes*60 + delta_str_seconds)/5)

                # here start first is the unresolved flight
                for i in range(len(shorterflight)):
                    SCREEN.blit(sector, (0, 0))

                    show_info(featurefile, index)
                    trajp = pred_trajectory(
                        dir_pred + '{}'.format(_d1), LIGHT_BLUE)

                    if i < offset:  # draw startfirst pixels only
                        pixels1 = to_pixels(
                            startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                        pygame.draw.circle(
                            SCREEN, color1, (pixels1[0], pixels1[1]), 3)

                        # flightname = font.render()
                        fpsClock.tick(FPS)
                        for event in pygame.event.get():
                            continue
                        # if event.type == pygame.MOUSEBUTTONDOWN:
                        # print(event.pos)
                        # keys = pygame.key.get_pressed()
                        accepted = accept.draw_button(SCREEN)
                        rejected = reject.draw_button(SCREEN)
                        nextclicked = next_scen.draw_button(SCREEN)
                        exitinterface = exitbutton.draw_button(SCREEN)
                        pygame.display.update()
                        # should not accept or reject at this stage so no conditions
                    else:
                        # condition when i > offset for unresolved flight starting first
                        pixels1 = to_pixels(
                            startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                        pygame.draw.circle(
                            SCREEN, color1, (pixels1[0], pixels1[1]), 3)
                        # startsecond is resolved flight with initial path
                        pixels2 = to_pixels(
                            startsecond.loc[i-offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])
                        pygame.draw.circle(
                            SCREEN, color2, (pixels2[0], pixels2[1]), 3)
                        pixels3 = to_pixels(
                            pred_res.loc[i-offset, 'longitude'], pred_res.loc[i - offset, 'latitude'])  # predicted

                        for event in pygame.event.get():
                            continue
                        pygame.display.update()
                        accepted = accept.draw_button(SCREEN)
                        rejected = reject.draw_button(SCREEN)
                        nextclicked = next_scen.draw_button(SCREEN)
                        exitinterface = exitbutton.draw_button(SCREEN)
                        # here the condition of maneuver initiation time should be added

                        if accepted == True and i - offset < steps:
                            print('Accpet pressed')
                            pygame.draw.circle(
                                SCREEN, color2, (pixels3[0], pixels3[1]), 3)
                            fpsClock.tick(FPS)
                            # break

                        elif rejected == True and i - offset < steps:
                            print('Rejected')
                            pygame.draw.circle(
                                SCREEN, color2, (pixels2[0], pixels2[1]), 3)

                        elif nextclicked == True:
                            print('NEXT')
                            break

                        elif exitinterface == True:
                            pygame.quit()

            else:
                startfirst = resflight
                startsecond = unresflight
                delta = pd.to_timedelta(
                    startsecond.loc[0, 'time']) - pd.to_timedelta(startfirst.loc[0, 'time'])
                delta_str_minutes = int(str(delta)[10:12])
                delta_str_seconds = int(str(delta)[13:])
                offset = int((delta_str_minutes*60 + delta_str_seconds)/5)

                for i in range(len(shorterflight)):  # startfirst is resolved
                    SCREEN.blit(sector, (0, 0))
                    trajp = pred_trajectory(
                        dir_pred + '{}'.format(_d1), LIGHT_BLUE)

                    if i < offset:  # draw startfirst pixels only
                        pixels1 = to_pixels(
                            startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                        pygame.draw.circle(
                            SCREEN, color1, (pixels1[0], pixels1[1]), 3)
                        pixels3 = to_pixels(
                            pred_res.loc[i, 'longitude'], pred_res.loc[i, 'latitude'])  # predicted
                        pygame.draw.circle(
                            SCREEN, color1, (pixels3[0], pixels3[1]), 3)
                        # flightname = font.render()
                        fpsClock.tick(FPS)
                        for event in pygame.event.get():
                            continue
                        # if event.type == pygame.MOUSEBUTTONDOWN:
                        # print(event.pos)
                        # keys = pygame.key.get_pressed()
                        accepted = accept.draw_button(SCREEN)
                        rejected = reject.draw_button(SCREEN)
                        nextclicked = next_scen.draw_button(SCREEN)
                        exitinterface = exitbutton.draw_button(SCREEN)
                        pygame.display.update()
                        # should not accept or reject at this stage so no conditions
                    else:
                        pixels1 = to_pixels(
                            startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])  # original resolved
                        pygame.draw.circle(
                            SCREEN, color1, (pixels1[0], pixels1[1]), 3)
                        pixels2 = to_pixels(
                            startsecond.loc[i-offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])  # unresolved
                        pygame.draw.circle(
                            SCREEN, color2, (pixels2[0], pixels2[1]), 3)
                        pixels3 = to_pixels(
                            pred_res.loc[i, 'longitude'], pred_res.loc[i, 'latitude'])  # predicted
                        fpsClock.tick(FPS)
                        for event in pygame.event.get():
                            continue
                        pygame.display.update()
                        accepted = accept.draw_button(SCREEN)
                        rejected = reject.draw_button(SCREEN)
                        nextclicked = next_scen.draw_button(SCREEN)
                        exitinterface = exitbutton.draw_button(SCREEN)
                        # here the condition of maneuver initiation time should be added

                        if accepted == True and i - offset < steps:
                            print('Accpet pressed')
                            pygame.draw.circle(
                                SCREEN, color2, (pixels3[0], pixels3[1]), 3)
                            # fpsClock.tick(FPS)
                            # break

                        elif rejected == True and i - offset < steps:
                            print('Rejected')
                            pygame.draw.circle(
                                SCREEN, color2, (pixels1[0], pixels1[1]), 3)

                        elif nextclicked == True:
                            print('NEXT')
                            break

                        elif exitinterface == True:
                            pygame.quit()

        else:
            shorterflight = resflight

            if pd.to_datetime(resflight.loc[0, 'time']) > pd.to_datetime(unresflight.loc[0, 'time']):
                startfirst = unresflight
                startsecond = resflight
                delta = pd.to_timedelta(
                    startsecond.loc[0, 'time']) - pd.to_timedelta(startfirst.loc[0, 'time'])
                delta_str_minutes = int(str(delta)[10:12])
                delta_str_seconds = int(str(delta)[13:])
                offset = int((delta_str_minutes*60 + delta_str_seconds)/5)

                # here start first is the unresolved flight
                for i in range(len(shorterflight)):
                    SCREEN.blit(sector, (0, 0))
                    trajp = pred_trajectory(
                        dir_pred + '{}'.format(_d1), LIGHT_BLUE)

                    if i < offset:  # draw startfirst pixels only
                        pixels1 = to_pixels(
                            startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])  # unresolved
                        pygame.draw.circle(
                            SCREEN, color1, (pixels1[0], pixels1[1]), 3)

                        # flightname = font.render()
                        fpsClock.tick(FPS)
                        for event in pygame.event.get():
                            continue
                        # if event.type == pygame.MOUSEBUTTONDOWN:
                        # print(event.pos)
                        # keys = pygame.key.get_pressed()
                        accepted = accept.draw_button(SCREEN)
                        rejected = reject.draw_button(SCREEN)
                        nextclicked = next_scen.draw_button(SCREEN)
                        exitinterface = exitbutton.draw_button(SCREEN)
                        pygame.display.update()
                        # should not accept or reject at this stage so no conditions
                    else:
                        # condition when i > offset for unresolved flight starting first
                        pixels1 = to_pixels(
                            startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])  # unresolved
                        pygame.draw.circle(
                            SCREEN, color1, (pixels1[0], pixels1[1]), 3)
                        # startsecond is resolved flight with initial path
                        pixels2 = to_pixels(
                            startsecond.loc[i-offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])  # resolved
                        pygame.draw.circle(
                            SCREEN, color2, (pixels2[0], pixels2[1]), 3)
                        pixels3 = to_pixels(
                            pred_res.loc[i-offset, 'longitude'], pred_res.loc[i - offset, 'latitude'])  # predicted

                        for event in pygame.event.get():
                            continue
                        fpsClock.tick(FPS)
                        pygame.display.update()
                        accepted = accept.draw_button(SCREEN)
                        rejected = reject.draw_button(SCREEN)
                        nextclicked = next_scen.draw_button(SCREEN)
                        exitinterface = exitbutton.draw_button(SCREEN)
                        # here the condition of maneuver initiation time should be added

                        if accepted == True and i - offset < steps:
                            print('Accpet pressed')
                            pygame.draw.circle(
                                SCREEN, color2, (pixels3[0], pixels3[1]), 3)
                            # fpsClock.tick(FPS)
                            # break

                        elif rejected == True and i - offset < steps:
                            print('Rejected')
                            pygame.draw.circle(
                                SCREEN, color2, (pixels2[0], pixels2[1]), 3)

                        elif nextclicked == True:
                            print('NEXT')
                            break

                        elif exitinterface == True:
                            pygame.quit()

                        pygame.display.update()

            else:
                startfirst = resflight
                startsecond = unresflight
                delta = pd.to_timedelta(
                    startsecond.loc[0, 'time']) - pd.to_timedelta(startfirst.loc[0, 'time'])
                delta_str_minutes = int(str(delta)[10:12])
                delta_str_seconds = int(str(delta)[13:])
                offset = int((delta_str_minutes*60 + delta_str_seconds)/5)

                for i in range(len(shorterflight)):  # startfirst is resolved
                    SCREEN.blit(sector, (0, 0))
                    trajp = pred_trajectory(
                        dir_pred + '{}'.format(_d1), LIGHT_BLUE)

                    if i < offset:  # draw startfirst pixels only
                        pixels1 = to_pixels(
                            startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                        pygame.draw.circle(
                            SCREEN, color1, (pixels1[0], pixels1[1]), 3)

                        pixels3 = to_pixels(
                            pred_res.loc[i, 'longitude'], pred_res.loc[i, 'latitude'])
                        pygame.draw.circle(
                            SCREEN, color1, (pixels3[0], pixels3[1]), 3)

                        # flightname = font.render()
                        fpsClock.tick(FPS)
                        for event in pygame.event.get():
                            continue
                        # if event.type == pygame.MOUSEBUTTONDOWN:
                        # print(event.pos)
                        # keys = pygame.key.get_pressed()
                        accepted = accept.draw_button(SCREEN)
                        rejected = reject.draw_button(SCREEN)
                        nextclicked = next_scen.draw_button(SCREEN)
                        exitinterface = exitbutton.draw_button(SCREEN)
                        pygame.display.update()
                        # should not accept or reject at this stage so no conditions
                    else:
                        # condition when i > offset for unresolved flight starting first
                        # resoved original
                        pixels1 = to_pixels(
                            startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                        pygame.draw.circle(
                            SCREEN, color1, (pixels1[0], pixels1[1]), 3)
                        pixels2 = to_pixels(
                            startsecond.loc[i-offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])  # unresolved
                        pygame.draw.circle(
                            SCREEN, color2, (pixels2[0], pixels2[1]), 3)
                        pixels3 = to_pixels(
                            pred_res.loc[i, 'longitude'], pred_res.loc[i, 'latitude'])  # predicted

                        for event in pygame.event.get():
                            continue
                        pygame.display.update()
                        accepted = accept.draw_button(SCREEN)
                        rejected = reject.draw_button(SCREEN)
                        nextclicked = next_scen.draw_button(SCREEN)
                        exitinterface = exitbutton.draw_button(SCREEN)
                        # here the condition of maneuver initiation time should be added

                        if accepted == True and i - offset < steps:
                            print('Accpet pressed')
                            pygame.draw.circle(
                                SCREEN, color1, (pixels3[0], pixels3[1]), 3)
                            # fpsClock.tick(FPS)
                            # break

                        elif rejected == True and i + offset < steps:
                            print('Rejected')
                            pygame.draw.circle(
                                SCREEN, color1, (pixels1[0], pixels1[1]), 3)

                        elif nextclicked == True:
                            print('NEXT')
                            break

                        elif exitinterface == True:
                            pygame.quit()
                        fpsClock.tick(FPS)

            pygame.display.update()

    return action
