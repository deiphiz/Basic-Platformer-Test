import pygame
import time
import random
from level import *
pygame.font.init()

#------------  R    G    B  ----------------
WHITE     =  (255, 255, 255)
GREY      =  (128, 128, 128)
BLACK     =  (  0,   0,   0)
RED       =  (255,   0,   0)
GREEN     =  (  0, 255,   0)
BLUE      =  (  0,   0, 255)
HOTPINK   =  (255, 110, 168)   
LIGHTBLUE =  (128, 128, 255)

BLOCK_COLOR = LIGHTBLUE
PLAYER_COLOR = HOTPINK
BACKGROUND_COLOR = BLACK
OSD_COLOR = WHITE

FONTSIZE = 20
MAINFONT = pygame.font.SysFont("Calibri", FONTSIZE)

def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawOSD(surface, strings):
    pos = 0
    for text in strings:
        drawText(text, MAINFONT, OSD_COLOR, surface, 10, pos)
        pos += FONTSIZE

def drawLevel(surface, camera):
    surface.fill(BACKGROUND_COLOR)

    # Rendering involves a little conversion of level coordinates to surface coordinates
    # The active area makes sure only blocks that are shown on screen are rendered
    for y in range(LEVELHEIGHT):
        for x in range(LEVELWIDTH):
            blockRect = pygame.Rect(x*BLOCKWIDTH, y*BLOCKHEIGHT, BLOCKWIDTH, BLOCKHEIGHT)
            if camera.colliderect(blockRect):
                if level[y][x] == BLANK:
                    continue
                if level[y][x] == BLOCK:
                    pygame.draw.rect(surface, BLOCK_COLOR, 
                    ((x*BLOCKWIDTH) - camera.left, 
                     (y*BLOCKHEIGHT) - camera.top, 
                     BLOCKWIDTH, 
                     BLOCKHEIGHT))
 
# This function is needed to draw a rect within the camera 
def drawRect(surface, rect, camera):
    pygame.draw.rect(surface, PLAYER_COLOR, (rect.left - camera.left, 
                                    rect.top - camera.top, 
                                    rect.width, 
                                    rect.height))