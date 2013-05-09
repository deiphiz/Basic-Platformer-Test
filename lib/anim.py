import pygame
import time

class Animation(object):
    def __init__(self, filename, spriteWidth, frameDuration):
        self.frameDuration = frameDuration
        
        # Set up spritesheet
        spritesheet = pygame.image.load(filename)
        spritesheetWidth, spritesheetHeight = spritesheet.get_size()
        
        # Make individual tiles
        self.frames = []
        for frame in range(spritesheetWidth/spriteWidth):
            newFrameRect = pygame.Rect(frame*spriteWidth, 
                                       0, 
                                       spriteWidth, 
                                       spritesheetHeight)
            self.frames.append(spritesheet.subsurface(newFrameRect))
        
        self.currentFrame = 0
        self.image = self.frames[self.currentFrame]
        self.lastFrame = time.time()
        self.reversed = False
            
    def update(self):
        if time.time() - self.lastFrame >= self.frameDuration:
            self.lastFrame = time.time()
            self.currentFrame += 1
            if self.currentFrame > len(self.frames)-1:
                self.currentFrame = 0
        self.image = self.frames[self.currentFrame]
    
    def reverse(self):
        for index, frame in enumerate(self.frames):
            self.frames[index] = pygame.transform.flip(frame, 1, 0)
        self.reversed = not self.reversed
        
    def reset(self):
        self.currentFrame = 0
        self.lastFrame = time.time()