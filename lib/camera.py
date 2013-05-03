import pygame
from level import *

CAMERASLACK = 60 # How much the target rect can move before the camera moves with it

class Camera(pygame.Rect):
    cameraSlack = 60
    def __init__(self, targetRect, windowWidth, windowHeight):
        super(Camera,self).__init__(targetRect.centerx-(windowWidth/2), 
                                    targetRect.centery-(windowHeight/2), 
                                    windowWidth, windowHeight)
        
    def update(self, rect, level):
        self.centerx = rect.centerx
        self.centery = rect.centery
        # Figure out if rect has exceeded camera slack
        if self.centerx - rect.centerx > CAMERASLACK:
            self.left = rect.centerx + CAMERASLACK - self.width/2
        elif rect.centerx - self.centerx > CAMERASLACK:
            self.left = rect.centerx - CAMERASLACK - self.width/2
        if self.centery - rect.centery > CAMERASLACK:
            self.top = rect.centery + CAMERASLACK - self.height/2
        elif rect.centery - self.centery > CAMERASLACK:
            self.top = rect.centery - CAMERASLACK - self.height/2
        
        # This keeps the camera within the boundaries of the level
        if self.right > level.rightEdge:
            self.right = level.rightEdge
        elif self.left < 0:
            self.left = 0
        if self.top < 0:
            self.top = 0
        elif self.bottom > level.bottomEdge:
            self.bottom = level.bottomEdge
        
        return self