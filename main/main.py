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
object = Player( 0, (100, 100), pos=vector2(200, 1000) )

object2 = Player( 1, (100, 100), (120, 0), RED )

ground = Ground( (1000, 25), pos=vector2(0, SCREEN_HEIGHT - 25))
ground2 = Ground( (25, 300), pos=vector2(500, 500))

sprite_manager.add( [ object, ground, ground2] )

# //MARK: MAIN LOOP
while Game_sys.running:
    for event in pg.event.get():

        controller_manager.translate_event( event )

        if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (event.type == pg.QUIT):
                Game_sys.running = False

    Game_sys.update()
    Game_sys.render()


    pg.display.flip()

    

    # print(Game_sys.clock.get_fps(), Game_sys.dt)

pg.quit()
