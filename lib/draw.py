import pygame
import time
import random
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

BLOCK_COLOR = WHITE
PLAYER_COLOR = HOTPINK
BACKGROUND_COLOR = BLACK
OSD_COLOR = GREY

FONTSIZE = 20
MAINFONT = pygame.font.SysFont("Courier New", FONTSIZE)
#BACKGROUND = pygame.transform.scale(pygame.image.load("lib\\background.jpg"), (800, 600))


def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_OSD(surface, strings):
    pos = 0
    for text in strings:
        drawText(text, MAINFONT, OSD_COLOR, surface, 10, pos)
        pos += FONTSIZE

def draw_level(surface, level, camera):
    #surface.blit(BACKGROUND, (0, 0))
    surface.fill(BACKGROUND_COLOR)

    # Rendering involves a little conversion of level coordinates to surface coordinates
    # The active area makes sure only blocks that are shown on screen are rendered
    for y in range(level.levelHeight):
        for x in range(level.levelWidth):
            blockRect = pygame.Rect(x*level.blockWidth, y*level.blockHeight, level.blockWidth, level.blockWidth)
            if camera.colliderect(blockRect):
                if level.collisionLayer[y][x] == level.blank:
                    continue
                if level.collisionLayer[y][x] == level.block:
                    surface.blit(level.blockSurf,
                                 ((x*level.blockWidth) - camera.left, 
                                 (y*level.blockHeight) - camera.top,))
                    #pygame.draw.rect(surface, BLOCK_COLOR, 
                    #((x*level.blockWidth) - camera.left, 
                     #(y*level.blockHeight) - camera.top, 
                     #level.blockWidth, 
                     #level.blockHeight))
 
# This function is needed to draw a rect within the camera 
def draw_entities(surface, sprites, camera):
    for sprite in sprites:
        surface.blit(sprite.image, (sprite.rect.left - camera.left, 
                                    sprite.rect.top - camera.top))