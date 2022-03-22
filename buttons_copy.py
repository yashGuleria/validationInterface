from matplotlib.pyplot import pause
import pygame
from pygame.locals import *

import time

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
pygame.init()
font = pygame.font.SysFont('Arial', 40)
pygame.font.init()

FPS = 5
fpsClock = pygame.time.Clock()

clicked = False


class Button():
    # global FPS
    button_color = (0, 255, 0)
    hover_color = (0, 0, 225)
    clicked_color = (255, 0, 0)
    text_color = (225, 225, 225)
    width = 180
    height = 40

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self, surface):

        global clicked
        action = False
        pos = pygame.mouse.get_pos()
        # print(pos)

        button_rect = Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(pos):
            pygame.draw.rect(surface, self.hover_color, button_rect)
            if not clicked:
                if len(pygame.event.get()) > 0 and pygame.mouse.get_pressed()[0]:
                    print('CLICK 11111')
                    # for _event in pygame.event.get():
                    # if _event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    action = True
                    pygame.draw.rect(
                        surface, self.clicked_color, button_rect)
        else:
            pygame.draw.rect(surface, self.button_color, button_rect)
            pass

        # if button_rect.collidepoint(pos):
        #     if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
        #         clicked = True
        #         action = True
        #         pygame.draw.rect(surface, self.clicked_color, button_rect)
        #     elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
        #         clicked = False  # reset trigger
        #         action = False
        #     else:
        #         pygame.draw.rect(surface, self.hover_color, button_rect)
        # else:
        #     pygame.draw.rect(surface, self.button_color, button_rect)

        # add shading to the buttons
        pygame.draw.line(surface, WHITE, (self.x, self.y),
                         (self.x + self.width, self.y), 2)
        pygame.draw.line(surface, WHITE, (self.x, self.y),
                         (self.x + self.width, self.y), 2)
        pygame.draw.line(surface, BLACK, (self.x, self.y + self.height),
                         (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(surface, BLACK, (self.x + self.width, self.y),
                         (self.x + self.width, self.y + self.height), 2)

        # add text to the button
        text_img = font.render(self.text, True, self.text_color)
        text_len = text_img.get_width()
        surface.blit(text_img, (self.x + int(self.width / 2) -
                                int(text_len / 2), self.y + 5))

        # fpsClock.tick(FPS)
        pygame.display.update()

        return action


class InfoButton():

    width = 180
    height = 40
    text_color = (0, 0, 0)

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self, surface):
        action = True
        pos = pygame.mouse.get_pos()

        button_rect = Rect(self.x, self.y, self.width, self.height)

        # add text to the button
        text_img = font.render(self.text, True, self.text_color)
        text_len = text_img.get_width()
        surface.blit(text_img, (self.x + int(self.width / 2) -
                                int(text_len / 2), self.y + 5))

        # fpsClock.tick(FPS)
        pygame.display.update()

        return action
