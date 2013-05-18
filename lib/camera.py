import pygame
from level import *

class Camera(pygame.Rect):
    cameraSlackX = 80
    cameraSlackY = 60
    def __init__(self, targetRect, windowWidth, windowHeight):
        super(Camera,self).__init__(targetRect.centerx-(windowWidth/2), 
                                    targetRect.centery-(windowHeight/2), 
                                    windowWidth, windowHeight)
        
    def update(self, rect, level):
        #self.centerx = rect.centerx
        #self.centery = rect.centery
        # Figure out if rect has exceeded camera slack
        if self.centerx - rect.centerx > self.cameraSlackX:
            self.left = rect.centerx + self.cameraSlackX - self.width/2
        elif rect.centerx - self.centerx > self.cameraSlackX:
            self.left = rect.centerx - self.cameraSlackX - self.width/2
        if self.centery - rect.centery > self.cameraSlackY:
            self.top = rect.centery + self.cameraSlackY - self.height/2
        elif rect.centery - self.centery > self.cameraSlackY:
            self.top = rect.centery - self.cameraSlackY - self.height/2
        
        # This keeps the camera within the boundaries of the level
        if self.right > level.rightEdge - level.blockWidth:
            self.right = level.rightEdge - level.blockWidth
        elif self.left < level.blockWidth:
            self.left = level.blockWidth
        if self.top < level.blockHeight*3:
            self.top = level.blockHeight*3
        elif self.bottom > level.bottomEdge:
            self.bottom = level.bottomEdge
        
        return self