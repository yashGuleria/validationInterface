import pygame
import random

FPS = 5
fpsClock = pygame.time.Clock()
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
YELLOW, PINK, INDIGO = (255, 255, 0), (255, 182, 193), (111, 0, 255)

pygame.init()
pygame.display.set_caption("Game TITLE")
screen = pygame.display.set_mode((400, 400))

myTextScore = 0
#font = pygame.font.Font('./Roboto-Regular.ttf',20)
font = pygame.font.SysFont(None, 20)
text = font.render("Score " + str(myTextScore), True, GREEN)

change_event = pygame.USEREVENT
pygame.time.set_timer(change_event, 500)  # 0.5 seconds
red_rect = pygame.Rect((random.randrange(1, 300)),
                       (random.randrange(1, 300)), 100, 100)

FPS = 100
fpsClock = pygame.time.Clock()
quitVar = True
while quitVar == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitVar = False

        if event.type == change_event:
            red_rect.x = (random.randrange(1, 300))
            red_rect.y = (random.randrange(1, 300))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if red_rect.collidepoint(event.pos):
                myTextScore += 1
                text = font.render("Score " + str(myTextScore), True, GREEN)

    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, red_rect)
    screen.blit(text, text.get_rect(center=(200, 350)))
    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
