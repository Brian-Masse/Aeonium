import pygame as pg
pg.init()


screen = pg.display.set_mode((800, 800) )

running = True

box = pg.Surface((100, 100))
box.fill( (255, 0, 0) )

x = 0

clock = pg.time.Clock()

while running:
    x += 5
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.QUIT:
            running = False

    screen.blit(box, ( x, 100 ))

    clock.tick(60)
    pg.display.flip()

pg.quit()