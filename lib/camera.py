import pygame
from level import *

CAMERASLACK = 60 # How much the target rect can move before the camera moves with it

def moveCamera(rect, camera):
    # Figure out if rect has exceeded camera slack
    if camera.centerx - rect.centerx > CAMERASLACK:
        camera.left = rect.centerx + CAMERASLACK - camera.width/2
    elif rect.centerx - camera.centerx > CAMERASLACK:
        camera.left = rect.centerx - CAMERASLACK - camera.width/2
    if camera.centery - rect.centery > CAMERASLACK:
        camera.top = rect.centery + CAMERASLACK - camera.height/2
    elif rect.centery - camera.centery > CAMERASLACK:
        camera.top = rect.centery - CAMERASLACK - camera.height/2
    
    # This keeps the camera within the boundaries of the level
    if camera.right > LEVELWIDTH*BLOCKWIDTH:
        camera.right = LEVELWIDTH*BLOCKWIDTH
    elif camera.left < 0:
        camera.left = 0
    if camera.top < 0:
        camera.top = 0
    elif camera.bottom > LEVELHEIGHT*BLOCKHEIGHT:
        camera.bottom = LEVELHEIGHT*BLOCKHEIGHT
    
    return camera