# Module for calculating jumps

FALLACCEL = 4
JUMPMOD = 2.5 # How much we subtract from the fall acceleration while jumping (helps to control the jump height)
JUMPACCEL = 25
MAXFALLSPEED = 30

def jump(speed, onBlock):
    if onBlock:
        speed -= JUMPACCEL
        
    # Gravity is decreased while jumping so the player can control
    # the height of his jump.
    speed += FALLACCEL - JUMPMOD
    
    # Simulate terminal velocity
    if speed > MAXFALLSPEED:
        speed = MAXFALLSPEED
    
    return speed
def fall(speed):
    speed += FALLACCEL
    
    # Simulate terminal velocity
    if speed > MAXFALLSPEED:
        speed = MAXFALLSPEED
        
    return speed