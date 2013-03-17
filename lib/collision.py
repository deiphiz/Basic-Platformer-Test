# Module for collision checking calculations

import pygame
import copy
from level import *

def checkLines(rect, axis):
    linesToCheck = []
    if axis == AXISX:
        for y in range(LEVELHEIGHT):
            if rect.colliderect(pygame.Rect(0, y*BLOCKHEIGHT, LEVELWIDTH*BLOCKWIDTH, BLOCKHEIGHT)):
                linesToCheck.append(y)
                
    elif axis == AXISY:
        for x in range(LEVELWIDTH):
            if rect.colliderect(pygame.Rect(x*BLOCKWIDTH, 0, BLOCKWIDTH, LEVELHEIGHT*BLOCKHEIGHT)):
                linesToCheck.append(x)
    
    return linesToCheck

def convertPixelToLevel(x, y):
    for levelX in range(LEVELWIDTH):
        for levelY in range(LEVELHEIGHT):
            tempRect = pygame.Rect(levelX * BLOCKWIDTH, levelY * BLOCKHEIGHT, BLOCKWIDTH, BLOCKHEIGHT)
            if tempRect.collidepoint(x, y):
                return (levelX, levelY)
                
def scanLine(line, start, end, dir, axis):
    if axis == AXISX:
        for tile in range(start, end, dir):
            if level[line][tile] == BLOCK:
                return tile
    elif axis == AXISY:
        for tile in range(start, end, dir):
            if level[tile][line] == BLOCK:
                return tile
    return start

# This function is the key to the collision detection algorithm.
# Basically, it calculates the distance between the "front" side of the player
# and the nearest obstacle on either the X axis or the Y axis.
#
# If that distance is shorter than the current speed of the player, then move by
# that distance instead.
def calculateDistance(coord, lines, dir):
    distances = []
    if dir == WEST or dir == EAST:
        playerTile = convertPixelToLevel(coord, 0)[0]
    elif dir == NORTH or dir == SOUTH:
        playerTile = convertPixelToLevel(0, coord)[1]
    
    # Which blocks are scanned are dependent on which direction the player is moving in.
    if dir == WEST:
        for line in lines:
            nearestBlock = scanLine(line, playerTile, -1, -1, AXISX)
            distances.append(abs(nearestBlock * BLOCKWIDTH + BLOCKWIDTH - coord))

    elif dir == EAST:
        for line in lines:
            nearestBlock = scanLine(line, playerTile, LEVELWIDTH, 1, AXISX)
            distances.append(abs(nearestBlock * BLOCKWIDTH - coord))
            
    elif dir == NORTH:
        for line in lines:
            nearestBlock = scanLine(line, playerTile, -1, -1, AXISY)
            distances.append(abs(nearestBlock * BLOCKHEIGHT + BLOCKHEIGHT - coord))
            
    elif dir == SOUTH:
        for line in lines:
            nearestBlock = scanLine(line, playerTile, LEVELHEIGHT, 1, AXISY)
            distances.append(abs(nearestBlock * BLOCKHEIGHT - coord))
    
    # The function should return the shortest or longest distance 
    # out of the lines which were checked depending on which 
    # direction the player was moving in.
    desiredValue = min(distances)
    if dir == WEST or dir == NORTH:
        return -desiredValue
    elif dir == EAST or dir == SOUTH:
        return desiredValue
        
def checkOnBlock(rect):
    for x in range(LEVELWIDTH):
        for y in range(LEVELHEIGHT):
            if level[y][x] == BLANK:
                continue
            elif level[y][x] == BLOCK:
                tempCheckRect = copy.deepcopy(rect)
                tempLevelRect = pygame.Rect(x*BLOCKWIDTH, y*BLOCKHEIGHT, BLOCKWIDTH, BLOCKHEIGHT)
                tempCheckRect.bottom += 1
                if tempLevelRect.colliderect(tempCheckRect):
                    return True 
                    
    return False 