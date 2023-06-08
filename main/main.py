import pygame as pg
pg.init()

from program.universals import*
from program.game_sys import*
from program.UI.text import*
from program.controller_manager import*

from program.player.rigid_body import*
from program.player.player import*

import math
import random

# objects
object = Player( 0, (100, 100) )
object2 = Player( 1, (100, 100), (120, 0), RED )
ground = Ground( (1000, 25), pos=(0, SCREEN_HEIGHT - 25))

sprite_manager.add( [ object, object2, ground ] )

# //MARK: MAIN LOOP
while Game_sys.running:
    for event in pg.event.get():

        controller_manager.translate_event( event )

        if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (event.type == pg.QUIT):
                Game_sys.running = False



    Game_sys.update()
    Game_sys.render()
    Game_sys.dt = Game_sys.clock.tick(FPS)
    pg.display.flip()

pg.quit()
