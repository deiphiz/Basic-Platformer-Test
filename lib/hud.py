import time

class OSD():
    def __init__(self):
        self.text = ['']
    
    def update(self, game):
        try:
            self.text = [\
            'BoxL: %r BoxR: %r BoxU: %r BoxD: %r' %(game.player.rect.left, 
                                                    game.player.rect.right, 
                                                    game.player.rect.top, 
                                                    game.player.rect.bottom),
            'Jumping: %r OnBlock: %r Crouching: %r' %(game.player.jumping, 
                                                      game.player.onBlock,
                                                      game.player.crouching),
            'deltaX: %r deltaY: %r' %(game.player.speedX, 
                                      game.player.speedY),
            'CameraX: %r CameraY: %r' %(game.cameraObj.left, 
                                        game.cameraObj.top),
            'MinX: %r MinY: %r' %(game.player.minXDistance,
                                  game.player.minYDistance),
            'Level Coordinates: %r, %r' %(game.player.get_coords(game.currentLevel)),
            'FPS: %r' %(int(game.clock.get_fps()))]
        except TypeError:
            self.text = ['ERROR']
