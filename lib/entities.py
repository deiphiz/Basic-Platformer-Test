import pygame
from pygame.locals import *
import copy
import time
import anim

Kleft = K_LEFT
Kright = K_RIGHT
Kjump = K_SPACE
Kcrouch = K_DOWN

NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
AXISX = 'x'
AXISY = 'y'

class Entity(object):
    color = (255, 0, 0)
    maxSpeed = 18
    accel_amt = 3
    airaccel_amt = 2
    deaccel_amt = 10
    
    fallAccel = 4
    jumpMod = 2.5
    jumpAccel = 25
    maxFallSpeed = 30
    
    def __init__(self, level, rectTuple, image=None):
        self.rect = pygame.Rect((rectTuple[0] * level.blockWidth) - level.blockWidth,
                                (rectTuple[1] * level.blockHeight) - level.blockHeight,
                                 rectTuple[2], rectTuple[3])
        self.normalHeight = self.rect.height

        self.cameraRect = copy.copy(self.rect)
        
        if type(image) is pygame.Surface:
            self.image = image
        elif type(image) is str:
            try:
                spritesheet = pygame.image.load(image)
            except pygame.error:
                self.image = pygame.Surface((self.rect.width, self.rect.height))
                self.image.fill(self.color)
        elif image == None:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(self.color)
        
        self.accelX = 0
        self.speedX = 0
        self.speedY = 0
        self.jumping = False
        self.onBlock = False
        
    def update(self):
        pass
        
    def load_frames(self, filename):
    
        # Set up spritesheet
        spritesheet = pygame.image.load(filename)
        spritesheetWidth, spritesheetHeight = spritesheet.get_size()
        
        # Make individual tiles
        frames = []
        for frame in range(spritesheetWidth/self.rect.width):
            newFrameRect = pygame.Rect(frame*self.rect.width, 
                                       0, 
                                       self.rect.width, 
                                       spritesheetHeight)
            frames.append(spritesheet.subsurface(newFrameRect))
        
        return frames
        
    def updateAnim(self):
        if time.time() - self.lastFrame >= 0.2:
            self.lastFrame = time.time()
            self.currentFrame += 1
            if self.currentFrame > len(self.frames)-1:
                self.currentFrame = 0
        self.image = self.frames[self.currentFrame]
        
    def get_accel(self, keys, jumping):
        if not jumping:
            return (keys[Kright] - keys[Kleft]) * self.accel_amt
        elif jumping:
            return (keys[Kright] - keys[Kleft]) * self.airaccel_amt
            
    def accelerate(self, accel, speed):
        if accel != 0:
            if ((speed < 0) and (accel > 0)) or\
               ((speed > 0) and (accel < 0)):
                speed = accel
            else:
                speed += accel
        
        if speed > self.maxSpeed:
            speed = self.maxSpeed
        if speed < -self.maxSpeed:
            speed = -self.maxSpeed

        if accel == 0:
            if speed > 0:
                speed -= self.deaccel_amt
                if speed < 0:
                    speed = 0
            if speed < 0:
                speed += self.deaccel_amt
                if speed > 0:
                    speed = 0

        return speed
        
    def jump(self, speed, onBlock):
        if onBlock:
            speed -= self.jumpAccel
            
        # Gravity is decreased while jumping so the player can control
        # the height of his jump.
        speed += self.fallAccel - self.jumpMod
        
        # Simulate terminal velocity
        if speed > self.maxFallSpeed:
            speed = self.maxFallSpeed
        
        return speed
    
    def fall(self, speed):
        speed += self.fallAccel
        
        # Simulate terminal velocity
        if speed > self.maxFallSpeed:
            speed = self.maxFallSpeed
            
        return speed
        
    def get_shortest_distance(self, rect, speed, axis, level):
        # Check which way the player is moving
        dir = self.check_dir(speed, axis)
        if dir == WEST:
            front = rect.left
        elif dir == EAST:
            front = rect.right
        elif dir == NORTH:
            front = rect.top
        elif dir == SOUTH:
            front = rect.bottom
        
        # Calculate the minimum distance
        linesToCheck = self.check_lines(rect, axis, level)
        if dir:
            minDistance = self.calculate_distance(front, linesToCheck, dir, level)
        else:
            minDistance = 0
        
        # If the minumum distance is shorter than the player's delta,
        # move the player by that distance instead.
        if self.check_collision(speed, minDistance):
            return minDistance
        else:
            return speed
            
    def check_dir(self, speed, axis):
        if axis == AXISX:
            if speed < 0:
                return WEST
            elif speed > 0:
                return EAST
                
        elif axis == AXISY:
            if speed < 0:
                return NORTH
            elif speed > 0:
                return SOUTH
                
    def check_lines(self, rect, axis, level):
        linesToCheck = []
        if axis == AXISX:
            for y in range(level.levelHeight):
                if rect.colliderect(pygame.Rect(0, 
                                                y*level.blockHeight, 
                                                level.rightEdge, 
                                                level.blockHeight)):
                    linesToCheck.append(y)
                    
        elif axis == AXISY:
            for x in range(level.levelWidth):
                if rect.colliderect(pygame.Rect(x*level.blockWidth, 
                                                0, 
                                                level.blockWidth, 
                                                level.bottomEdge)):
                    linesToCheck.append(x)
        
        return linesToCheck
    
    def calculate_distance(self, coord, lines, dir, level):
        distances = []
        if dir == WEST or dir == EAST:
            playerTile = self.convert_pixel_to_level(coord, 0, level)[0]
        elif dir == NORTH or dir == SOUTH:
            playerTile = self.convert_pixel_to_level(0, coord, level)[1]
        
        # Which blocks are scanned are dependent on which direction the player is moving in.
        if dir == WEST:
            for line in lines:
                nearestBlock = self.scan_line(line, playerTile, -1, -1, AXISX, level)
                distances.append(abs(nearestBlock * level.blockWidth + level.blockWidth - coord))

        elif dir == EAST:
            for line in lines:
                nearestBlock = self.scan_line(line, playerTile, level.levelWidth, 1, AXISX, level)
                distances.append(abs(nearestBlock * level.blockWidth - coord))
                
        elif dir == NORTH:
            for line in lines:
                nearestBlock = self.scan_line(line, playerTile, -1, -1, AXISY, level)
                distances.append(abs(nearestBlock * level.blockHeight + level.blockHeight - coord))
                
        elif dir == SOUTH:
            for line in lines:
                nearestBlock = self.scan_line(line, playerTile, level.levelHeight, 1, AXISY, level)
                distances.append(abs(nearestBlock * level.blockHeight - coord))
        
        # The function should return the shortest or longest distance 
        # depending on which direction the player was moving in.
        desiredValue = min(distances)
        if dir == WEST or dir == NORTH:
            return -desiredValue
        elif dir == EAST or dir == SOUTH:
            return desiredValue
            
    def convert_pixel_to_level(self, x, y, level):
        for levelX in range(level.levelWidth):
            for levelY in range(level.levelHeight):
                tempRect = pygame.Rect(levelX * level.blockWidth, 
                                       levelY * level.blockHeight, 
                                       level.blockWidth, level.blockHeight)
                if tempRect.collidepoint(x, y):
                    return (levelX, levelY)
    
    def scan_line(self, line, start, end, dir, axis, level):
        if axis == AXISX:
            for tile in range(start, end, dir):
                if level.collisionLayer[line][tile] == level.block:
                    return tile
        elif axis == AXISY:
            for tile in range(start, end, dir):
                if level.collisionLayer[tile][line] == level.block:
                    return tile
        return start
        
    def check_collision(self, speed, minDistance):
        # If minumum X distance is shorter than the player's deltaX,
        # move the player by that distance instead.
        if (speed < 0 and minDistance > speed) or\
           (speed > 0 and minDistance < speed):
           return True
                
        return False
        
    def check_on_block(self, rect, level):
        for x in range(level.levelWidth):
            for y in range(level.levelHeight):
                if level.collisionLayer[y][x] == level.blank:
                    continue
                elif level.collisionLayer[y][x] == level.block:
                    tempCheckRect = copy.copy(rect)
                    tempLevelRect = pygame.Rect(x*level.blockWidth, 
                                                y*level.blockHeight, 
                                                level.blockWidth, level.blockHeight)
                    tempCheckRect.bottom += 1
                    if tempLevelRect.colliderect(tempCheckRect):
                        return True 
                        
        return False
        
    def get_coords(self, level):
        return self.convert_pixel_to_level(self.rect.centerx, self.rect.centery, level)
        
class Player(Entity):
    crouching = False
    crouchHeight = 70
    def __init__(self, level, rectTuple, image=None):
        super(Player, self).__init__(level, rectTuple, image)
        try:
            self.runAnim = anim.Animation("lib\\player.png", self.rect.width, 0.05)
            self.crouchAnim = anim.Animation("lib\\crouching.png", self.rect.width, 0.05)
            self.hasAnim = True
        except pygame.error:
            self.hasAnim = False
    def update(self, keys, level):
        # Crouch the player if needed
        if keys[Kcrouch] and not self.crouching:
            self.crouching = True
            self.rect.height = self.crouchHeight
            self.rect.bottom += self.normalHeight - self.crouchHeight
        elif not keys[Kcrouch] and self.crouching:
            self.crouching = False
            self.rect.height = self.normalHeight
            self.rect.bottom -= self.normalHeight - self.crouchHeight
        
        # Update the player's image to the new rect size
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        
        # Calculate movement on X-axis
        self.accelX = self.get_accel(keys, self.jumping)
        self.speedX = self.accelerate(self.accelX, self.speedX)
        
        # Calculate movement on Y-axis
        self.jumping = keys[Kjump]
        self.onBlock = self.check_on_block(self.rect, level)
        if self.jumping:
            self.speedY = self.jump(self.speedY, self.onBlock)
            if self.onBlock:
                self.onBlock == True
        else:
            self.speedY = self.fall(self.speedY)
            
        # Check if player needs to be stopped at an obstacle:
        # For X-axis
        try:
            self.minXDistance = self.get_shortest_distance(self.rect, self.speedX, AXISX, level)
        except (TypeError, IndexError, ValueError):
            self.minXDistance = self.speedX
        if abs(self.minXDistance) < abs(self.speedX):
            self.speedX = 0
        
        # For Y-axis
        try:
            self.minYDistance = self.get_shortest_distance(self.rect, self.speedY, AXISY, level)
        except (TypeError, IndexError, ValueError):
            self.minYDistance = self.speedY
        if abs(self.minYDistance) < abs(self.speedY):
            self.speedY = 0
        
        # Update player position
        self.rect.left += self.minXDistance  
        self.rect.top  += self.minYDistance
        self.cameraRect.move_ip(self.minXDistance, self.minYDistance)
        
        # Update frames of player if possible
        if self.hasAnim:
            if self.speedX > 0:
                if self.runAnim.reversed or self.crouchAnim.reversed:
                    self.runAnim.reverse()
                    self.crouchAnim.reverse()
                self.runAnim.update()
                self.image = self.runAnim.image
            elif self.speedX < 0:
                if not self.runAnim.reversed or not self.crouchAnim.reversed:
                    self.runAnim.reverse()
                    self.crouchAnim.reverse()
                    
            if not self.crouching:        
                self.runAnim.update()
                self.image = self.runAnim.image
            elif self.crouching:
                self.crouchAnim.update()
                self.image = self.crouchAnim.image
                
            if self.speedY != 0 or self.jumping:
                self.image = self.runAnim.frames[4]
            elif self.speedX == 0 and self.speedY == 0:
                if not self.crouching:
                    self.image = self.runAnim.frames[0]
                elif self.crouching:
                    self.image = self.crouchAnim.frames[0]
                self.runAnim.reset()
                self.crouchAnim.reset()