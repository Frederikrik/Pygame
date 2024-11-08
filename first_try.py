# main file for coding
import pygame
import random 
import sys
# initialize pygame
pygame.init()

size = width, height = 450, 300
score=0
player = 50
black = 0,0,0

screen = pygame.display.set_mode(size)
pygame.display.set_caption ("Cowboy game")
#background= black
background = pygame.image.load ("background.png")
# adapt the screen to the picture
background = pygame.transform.scale(background, (width, height))
fps = 60
font= pygame.font.Font("freesansbold.ttf", 16)
# do we need a timer?
timer = pygame.time.Clock()

running = True
while running:
    timer.tick (fps)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
         running = False   

    pygame.display.flip()
pygame.quit()
sys.exit()