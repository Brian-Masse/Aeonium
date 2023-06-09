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

player_size = ( 100, 200 )

# objects
player1 = Player( 0, player_size, vector2(200, 100), BLUE)
player2 = Player( 1, player_size, vector2(SCREEN_WIDTH - 200, 100), RED )

ground = Ground( (SCREEN_WIDTH, 50), pos=vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 25))
ground2 = Ground( (200, 20), pos=vector2(500, 500))

sprite_manager.add( [ player1, player2, ground, ground2] )

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
