import pygame
from level import *

class Camera(pygame.Rect):
    cameraSlack = 60
    def __init__(self, targetRect, windowWidth, windowHeight):
        super(Camera,self).__init__(targetRect.centerx-(windowWidth/2), 
                                    targetRect.centery-(windowHeight/2), 
                                    windowWidth, windowHeight)
        
    def update(self, rect, level):
        #self.centerx = rect.centerx
        #self.centery = rect.centery
        # Figure out if rect has exceeded camera slack
        if self.centerx - rect.centerx > self.cameraSlack:
            self.left = rect.centerx + self.cameraSlack - self.width/2
        elif rect.centerx - self.centerx > self.cameraSlack:
            self.left = rect.centerx - self.cameraSlack - self.width/2
        if self.centery - rect.centery > self.cameraSlack:
            self.top = rect.centery + self.cameraSlack - self.height/2
        elif rect.centery - self.centery > self.cameraSlack:
            self.top = rect.centery - self.cameraSlack - self.height/2
        
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