# Module for calculating jumps

FALLACCEL = 5
JUMPMOD = 3 # How much we subtract from the fall acceleration while jumping (helps to control the jump height)
JUMPACCEL = 31
MAXFALLSPEED = 40

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