"""
    My test for 2D platformer movement.
    Here we have collision detection, smooth accelerated movement,
    seperate world and window coordinates, and camera movement.
    
    I've completely refactored this code in this version, and split
    up many things into different modules.
"""

import pygame
import sys
import time
from lib import collision, movement, draw, camera, jump
from lib.level import *
from pygame.locals import *
pygame.init()

# Screen Constants
FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FLAGS = HWSURFACE|DOUBLEBUF

def main():
    
    # Set in-game variables
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FLAGS)
    pygame.display.set_caption('2D Platforming Test 3')
    clock = pygame.time.Clock()
    
    # Set up entities
    player = pygame.Rect(10*BLOCKWIDTH, 
                         12*BLOCKHEIGHT - 300, 
                         PLAYERSIZE, PLAYERSIZE)
    cameraRect = pygame.Rect(player.centerx-(WINDOWWIDTH/2), 
                      player.centery-(WINDOWHEIGHT/2), 
                      WINDOWWIDTH, WINDOWHEIGHT)
    
    # Set up in-game variables
    accelX = 0
    playerSpeedX = 0
    playerSpeedY = 0
    jumping = False
    onBlock = False
    showText = True

    # Start game loop
    while True:

    #///////////////////////Event handling///////////////////////#
        for event in pygame.event.get():
            if event.type == QUIT or\
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE and not jumping:
                    jumping = True
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    jumping = False
                if event.key == K_x:
                    showText = not showText
                if event.key == K_c:
                    level = open("level.lvl").readlines()

        Xkeys = pygame.key.get_pressed()
        accelX = movement.getAccel(Xkeys, jumping)

    #///////////////////////X-axis movement///////////////////////#

        # playerSpeedX is calculated seperately just in case we 
        # want movement without acceleration in the future
        playerSpeedX = movement.accelerate(accelX, playerSpeedX)
        minXDistance = movement.getSmallestDistance(player, playerSpeedX, AXISX)
        player.left += minXDistance
        if abs(minXDistance) < abs(playerSpeedX):
            playerSpeedX = 0
        
    #///////////////////////Y-axis movement///////////////////////#
        
        onBlock = collision.checkOnBlock(player)
        if jumping:
            playerSpeedY = jump.jump(playerSpeedY, onBlock)
            if onBlock:
                onBlock = False
        else:
            playerSpeedY = jump.fall(playerSpeedY)
        
        minYDistance = movement.getSmallestDistance(player, playerSpeedY, AXISY)
        player.top += minYDistance
        if abs(minYDistance) < abs(playerSpeedY):
            playerSpeedY = 0

    #///////////////////////Camera Movement///////////////////////#
        
        cameraRect = camera.moveCamera(player, cameraRect)
        # Uncomment below to have the camera always locked to the player
        # cameraRect.topleft = (player.centerx-(WINDOWWIDTH/2), player.centery-(WINDOWHEIGHT/2))
            
    #///////////////////////Rendering///////////////////////#
        
        draw.drawLevel(screen, cameraRect)
        draw.drawRect(screen, player, cameraRect)

        if showText:
            # Customise the OSD here. This was the information I found the most useful.
            OSDText = [\
            'BoxL: %r BoxR: %r BoxU: %r BoxD: %r' %(player.left, player.right, player.top, player.bottom),
            'Jumping: %r OnBlock: %r' %(jumping, onBlock),
            'deltaX: %r deltaY: %r' %(playerSpeedX, playerSpeedY),
            #'minX: %r minY: %r' %(minXDistance, minYDistance),
            'CameraX: %r CameraY: %r' %(cameraRect.left, cameraRect.top),
            'Level Coordinates: %r, %r' %(collision.convertPixelToLevel(player.left, player.top))]
            
            draw.drawOSD(screen, OSDText)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()