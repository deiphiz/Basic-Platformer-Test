# Simple collision layer parser
# Also keeps some level related constants
import pygame

# Parse level-----------------
BLANK = '.'
BLOCK = '0'
level = [row.strip('\n') for row in\
         open("level.lvl", 'r').readlines()]

# Syntatic sugars-------------
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
AXISX = 'x'
AXISY = 'y'
        
# Set level constants-----------       
LEVELWIDTH = len(level[0])
LEVELHEIGHT = len(level)
BLOCKWIDTH = 75
BLOCKHEIGHT = 75

# Player-----------------------
PLAYERSIZE = 50