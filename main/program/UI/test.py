import pygame

pygame.init()

running = True


screen_width = 1440
screen_height = 860
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.RESIZABLE)

surface = pygame.Surface(( 100, 100 ))
surface.fill( (255, 0, 0) )

x = 0

while running:
    x += 0.5

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    screen.blit( surface, (x, 100) )

    pygame.display.flip()

pygame.quit()