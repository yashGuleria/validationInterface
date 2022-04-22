import pygame
from pygame.locals import *

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
font = pygame.font.SysFont('Constantia', 35)
font2 = pygame.font.SysFont('Arial', 35)
font3 = pygame.font.SysFont('Arial', 14)

pygame.font.init()

FPS = 3
fpsClock = pygame.time.Clock()

clicked = False


class Button():
    # global FPS
    button_color = (25, 190, 225)
    hover_color = (75, 225, 225)
    clicked_color = (50, 150, 225)
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
            if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                clicked = True
                action = True
                pygame.draw.rect(surface, self.clicked_color, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False  # reset trigger
                action = False
            else:
                pygame.draw.rect(surface, self.hover_color, button_rect)
        else:
            pygame.draw.rect(surface, self.button_color, button_rect)
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
        text_img = font2.render(self.text, True, self.text_color)
        text_len = text_img.get_width()
        surface.blit(text_img, (self.x + int(self.width / 2) -
                                int(text_len / 2), self.y + 5))

        # fpsClock.tick(FPS)
        pygame.display.update()

        return action


class FlightDataButton():
    """to draw the flight information data block"""
    width = 2
    height = 1
    text_color = (0, 0, 0)

    def __init__(self, x, y, flightinfo): #flightinfo should be a list [callsign, FL, speed]
        self.x = x #longitudess
        self.y = y #latitude
        self.flightinfo = flightinfo

    def draw_button(self, surface):
        button_rect = Rect(self.x, self.y, self.width, self.height)

        txt_img1 = font3.render(self.flightinfo[0], True, self.text_color)
        txt_len1 = txt_img1.get_width()
        surface.blit(txt_img1, (self.x + int(self.width / 2) -
                                int(txt_len1 / 2), self.y + 2))

        txt_img2 = font3.render((self.flightinfo[1] + '  ' +self.flightinfo[2]), True, self.text_color)
        txt_len2 = txt_img2.get_width()
        surface.blit(txt_img2, (self.x + int(self.width / 2) -int(txt_len2 / 2), self.y + 20))

        pygame.display.update()
        
