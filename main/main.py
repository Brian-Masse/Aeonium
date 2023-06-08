import pygame as pg
pg.init()

# from program.universals import*
from program.game_sys import*
from program.rigid_body import*
from program.UI.text import*

import math
import random

# objects
object = Rigid_Body( (100, 100) )
ground = Ground( (1000, 25), pos=(0, SCREEN_HEIGHT - 25))

sprite_manager.add( [ object, ground ] )

# //MARK: MAIN LOOP
while Game_sys.running:
    for event in pg.event.get():
        if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (event.type == pg.QUIT):
                Game_sys.running = False

    Game_sys.update()
    Game_sys.render()
    Game_sys.dt = Game_sys.clock.tick(FPS)
    pg.display.flip()

pg.quit()
