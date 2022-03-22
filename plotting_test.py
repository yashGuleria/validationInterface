import numpy as np
import pandas as pd
# from buttons_copy import Button, InfoButton
import os
import sys
from utils import *
from buttons import Button, InfoButton


from matplotlib.pyplot import pause

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


def line_evolve(sorted_resdir, sorted_unresdir, sorted_preddir, color1, color2):
    action = True

    featurefile = pd.read_csv('featurefile_110222set1.csv')

    for index, (_d1, _d2, _d3) in enumerate(zip(sorted_resdir, sorted_unresdir, sorted_preddir)):

        resolution_accepted = False
        resolution_rejected = False
        next_scenario = False

        resflight = pd.read_csv(dir_res + '{}'.format(_d1))
        unresflight = pd.read_csv(dir_unres + '{}'.format(_d2))
        pred_res = pd.read_csv(dir_pred + '{}'.format(_d3))
        print(_d1, _d2, _d3)

        resflight_t, unresflight_t, pred_res_t = trimmed_flights(
            resflight, unresflight, pred_res)
        SCREEN.fill(PASTEL_BLUE)
        SCREEN.blit(sector, (0, 0))
        show_info(featurefile, index)
        # draw maneuver information

        # pygame.display.update()

        # calculating timesteps to maneuver initiation
        for f in range(len(featurefile)):
            if _d1 == featurefile.loc[f, 'resolvedflight']:
                maneuv_time = featurefile.loc[f, 'timetoresolution']
                steps = int((maneuv_time * 60) / 5)
                # print(' maneuver initiation steps:  ', steps)
                break
        print('STEPS :', steps)

        if pd.to_datetime(resflight_t.loc[0, 'time']) > pd.to_datetime(unresflight_t.loc[0, 'time']):
            startfirst = unresflight_t
            startsecond = resflight_t
            delta = pd.to_timedelta(
                startsecond.loc[0, 'time']) - pd.to_timedelta(startfirst.loc[0, 'time'])
            delta_str_minutes = int(str(delta)[10:12])
            delta_str_seconds = int(str(delta)[13:])
            os1 = 0
            os2 = int((delta_str_minutes*60 + delta_str_seconds)/5)
            offset = os2
            # here start first is the unresolved flight
            print('OFFSET :', offset)

            for i in range(offset+1):
                SCREEN.blit(sector, (0, 0))
                trajp = pred_trajectory(
                    dir_pred + '{}'.format(_d1), LIGHT_BLUE)

                pixels1 = to_pixels(
                    startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                pygame.draw.circle(SCREEN, color1, (pixels1[0], pixels1[1]), 3)
                fpsClock.tick(FPS)
                # if len(pygame.event.get()):
                #     pass
                # for event in pygame.event.get():
                #     continue
                accepted = accept.draw_button(SCREEN)
                rejected = reject.draw_button(SCREEN)
                nextclicked = next_scen.draw_button(SCREEN)
                exitinterface = exitbutton.draw_button(SCREEN)
                pygame.display.update()

            # for i in range(offset, steps):
            #     accepted = accept.draw_button(SCREEN)
            #     # print(accept)
            #     rejected = reject.draw_button(SCREEN)
            #     nextclicked = next_scen.draw_button(SCREEN)
            #     exitinterface = exitbutton.draw_button(SCREEN)

            #     if accepted:
            #         print('GET TRUE CLICK')
            #         resolution_accepted = True
            #         break
            #     # if not accept:
            #     #     pause(0.01)

                # else:
                # resolution_accepted == False
            # print('resolution_accepted: ', resolution_accepted)

            for i in range(offset, steps-offset):
                accepted = accept.draw_button(SCREEN)
                # print(accept)
                rejected = reject.draw_button(SCREEN)
                nextclicked = next_scen.draw_button(SCREEN)
                exitinterface = exitbutton.draw_button(SCREEN)

                if accepted:
                    print('RESOLUTION ACCEPTED')
                    resolution_accepted = True

                if rejected:
                    print("RESOLUTION REJECTED")
                    resolution_rejected = True

                SCREEN.blit(sector, (0, 0))
                trajp = pred_trajectory(
                    dir_pred + '{}'.format(_d1), LIGHT_BLUE)
                pixel1 = to_pixels(
                    startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                pygame.draw.circle(SCREEN, BLACK, (pixel1[0], pixel1[1]), 3)

                pixel2 = to_pixels(
                    startsecond.loc[i - offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])
                pygame.draw.circle(SCREEN, RED, (pixel2[0], pixel2[1]), 3)

                for event in pygame.event.get():
                    continue
                fpsClock.tick(FPS)
                pygame.display.update()

            for i in range(steps-offset, len(startfirst)):
                SCREEN.blit(sector, (0, 0))
                trajp = pred_trajectory(
                    dir_pred + '{}'.format(_d1), LIGHT_BLUE)
                pixel1 = to_pixels(
                    startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                pygame.draw.circle(SCREEN, BLACK, (pixel1[0], pixel1[1]), 3)

                if resolution_accepted == True:
                    print("MODIFIED")
                    pixel2 = to_pixels(
                        pred_res_t.loc[i - offset, 'longitude'], pred_res_t.loc[i - offset, 'latitude'])
                    pygame.draw.circle(SCREEN, RED, (pixel2[0], pixel2[1]), 3)
                    accepted = accept.draw_button(SCREEN)
                    rejected = reject.draw_button(SCREEN)
                    nextclicked = next_scen.draw_button(SCREEN)
                    exitinterface = exitbutton.draw_button(SCREEN)
                    for event in pygame.event.get():
                        continue
                    fpsClock.tick(FPS)
                    pygame.display.update()

                elif nextclicked:
                    break

                else:  # this is the rejected condition
                    pixel2 = to_pixels(
                        startsecond.loc[i - offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])
                    pygame.draw.circle(SCREEN, RED, (pixel2[0], pixel2[1]), 3)
                    accepted = accept.draw_button(SCREEN)
                    rejected = reject.draw_button(SCREEN)
                    nextclicked = next_scen.draw_button(SCREEN)
                    exitinterface = exitbutton.draw_button(SCREEN)
                    for event in pygame.event.get():
                        continue
                    fpsClock.tick(FPS)
                    pygame.display.update()

            pygame.display.update()

        else:
            startfirst = resflight_t
            startsecond = unresflight_t

            delta = pd.to_timedelta(
                startsecond.loc[0, 'time']) - pd.to_timedelta(startfirst.loc[0, 'time'])
            delta_str_minutes = int(str(delta)[10:12])
            delta_str_seconds = int(str(delta)[13:])
            os1 = 0
            os2 = int((delta_str_minutes*60 + delta_str_seconds)/5)
            offset = os2
            # here start first is the unresolved flight
            print('OFFSET :', offset)

            for i in range(offset+1):
                SCREEN.blit(sector, (0, 0))
                trajp = pred_trajectory(
                    dir_pred + '{}'.format(_d1), LIGHT_BLUE)

                pixels1 = to_pixels(
                    startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                pygame.draw.circle(SCREEN, color1, (pixels1[0], pixels1[1]), 3)
                fpsClock.tick(FPS)
                # if len(pygame.event.get()):
                #     pass
                # for event in pygame.event.get():
                #     continue
                accepted = accept.draw_button(SCREEN)
                rejected = reject.draw_button(SCREEN)
                nextclicked = next_scen.draw_button(SCREEN)
                exitinterface = exitbutton.draw_button(SCREEN)
                pygame.display.update()

            # for i in range(offset, steps):
            #     accepted = accept.draw_button(SCREEN)
            #     # print(accept)
            #     rejected = reject.draw_button(SCREEN)
            #     nextclicked = next_scen.draw_button(SCREEN)
            #     exitinterface = exitbutton.draw_button(SCREEN)

            #     if accepted:
            #         print('GET TRUE CLICK')
            #         resolution_accepted = True
            #         break
                # if not accept:
                #     pause(0.01)

                # else:
                # resolution_accepted == False
            # print('resolution_accepted: ', resolution_accepted)

            for i in range(offset, steps):
                accepted = accept.draw_button(SCREEN)
                # print(accept)
                rejected = reject.draw_button(SCREEN)
                nextclicked = next_scen.draw_button(SCREEN)
                exitinterface = exitbutton.draw_button(SCREEN)

                if accepted:
                    print('RESOLUTION ACCEPTED')
                    resolution_accepted = True

                if rejected:
                    print("RESOLUTION REJECTED")
                    resolution_rejected = True

                SCREEN.blit(sector, (0, 0))
                trajp = pred_trajectory(
                    dir_pred + '{}'.format(_d1), LIGHT_BLUE)
                pixel1 = to_pixels(
                    startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                pygame.draw.circle(SCREEN, BLACK, (pixel1[0], pixel1[1]), 3)

                pixel2 = to_pixels(
                    startsecond.loc[i - offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])
                pygame.draw.circle(SCREEN, RED, (pixel2[0], pixel2[1]), 3)

                for event in pygame.event.get():
                    continue
                fpsClock.tick(FPS)
                pygame.display.update()

            for i in range(steps, len(startfirst)):
                SCREEN.blit(sector, (0, 0))
                trajp = pred_trajectory(
                    dir_pred + '{}'.format(_d1), LIGHT_BLUE)

                if resolution_accepted == True:
                    print("MODIFIED")

                    pixel1 = to_pixels(
                        pred_res_t.loc[i, 'longitude'], pred_res_t.loc[i, 'latitude'])
                    pygame.draw.circle(
                        SCREEN, BLACK, (pixel1[0], pixel1[1]), 3)
                    pixel2 = to_pixels(
                        startsecond.loc[i - offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])
                    pygame.draw.circle(SCREEN, RED, (pixel2[0], pixel2[1]), 3)
                    accepted = accept.draw_button(SCREEN)
                    rejected = reject.draw_button(SCREEN)
                    nextclicked = next_scen.draw_button(SCREEN)
                    exitinterface = exitbutton.draw_button(SCREEN)
                    for event in pygame.event.get():
                        continue
                    fpsClock.tick(FPS)
                    pygame.display.update()

                elif nextclicked:
                    break

                else:
                    pixel1 = to_pixels(
                        startfirst.loc[i, 'longitude'], startfirst.loc[i, 'latitude'])
                    pygame.draw.circle(
                        SCREEN, BLACK, (pixel1[0], pixel1[1]), 3)
                    pixel2 = to_pixels(
                        startsecond.loc[i - offset, 'longitude'], startsecond.loc[i - offset, 'latitude'])
                    pygame.draw.circle(SCREEN, RED, (pixel2[0], pixel2[1]), 3)
                    accepted = accept.draw_button(SCREEN)
                    rejected = reject.draw_button(SCREEN)
                    nextclicked = next_scen.draw_button(SCREEN)
                    exitinterface = exitbutton.draw_button(SCREEN)
                    for event in pygame.event.get():
                        continue
                    fpsClock.tick(FPS)
                    pygame.display.update()

            pygame.display.update()

    return action
