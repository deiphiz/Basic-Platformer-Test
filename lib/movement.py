# Module for calculating movement distances

import collision
from level import *
from pygame.locals import *

ACCEL = 3
AIRACCEL = 2
DEACCEL = 10
MAXSPEED = 18

def getAccel(keys, jumping):
    if not jumping:
        return (keys[K_RIGHT] - keys[K_LEFT]) * ACCEL
    elif jumping:
        return (keys[K_RIGHT] - keys[K_LEFT]) * AIRACCEL

def checkDir(speed, axis):
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

def checkCollision(speed, minDistance):
    # If minumum X distance is shorter than the player's deltaX,
    # move the player by that distance instead.
    if (speed < 0 and minDistance > speed) or\
       (speed > 0 and minDistance < speed):
       return True
            
    return False

def accelerate(accel, speed):
    if accel != 0:
        if ((speed < 0) and (accel > 0)) or\
           ((speed > 0) and (accel < 0)):
            speed = accel
        else:
            speed += accel
    
    if speed > MAXSPEED:
        speed = MAXSPEED
    if speed < -MAXSPEED:
        speed = -MAXSPEED

    if accel == 0:
        if speed > 0:
            speed -= DEACCEL
            if speed < 0:
                speed = 0
        if speed < 0:
            speed += DEACCEL
            if speed > 0:
                speed = 0

    return speed
    
def getSmallestDistance(rect, speed, axis):
    # Check which way the player is moving
    dir = checkDir(speed, axis)
    if dir == WEST:
        front = rect.left
    elif dir == EAST:
        front = rect.right
    elif dir == NORTH:
        front = rect.top
    elif dir == SOUTH:
        front = rect.bottom
    
    # Calculate the minimum distance
    linesToCheck = collision.checkLines(rect, axis)
    if dir:
        minDistance = collision.calculateDistance(front, linesToCheck, dir)
    else:
        minDistance = 0
    
    # If the minumum distance is shorter than the player's delta,
    # move the player by that distance instead.
    if checkCollision(speed, minDistance):
        return minDistance
    else:
        return speed