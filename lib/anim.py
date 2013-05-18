import pygame
import time

class Animation(object):
    def __init__(self, image, spriteWidth, frameDuration):
        self.frameDuration = frameDuration
        
        # Set up spritesheet
        if type(image) is str:
            spritesheet = pygame.image.load(image)
        elif type(image) is pygame.Surface:
            spritesheet = image
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
        elapsed = time.time() - self.lastFrame
        if elapsed >= self.frameDuration:
            self.lastFrame = time.time()
            self.currentFrame += 1
            while self.currentFrame > len(self.frames)-1:
                self.currentFrame = 0
        self.image = self.frames[int(self.currentFrame)]
    
    def reverse(self):
        for index, frame in enumerate(self.frames):
            self.frames[index] = pygame.transform.flip(frame, 1, 0)
        self.reversed = not self.reversed
        
    def reset(self):
        self.currentFrame = 0
        self.lastFrame = time.time()