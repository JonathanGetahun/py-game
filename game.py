import pygame, sys
pygame.init()
screen = pygame.display.set_mode((576, 924))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/ville.png').convert()
#bg_surface = pygame.transform.scale(bg_surface, (900, 900))

floor_surface = pygame.image.load

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(bg_surface,(0,-300))
    
    pygame.display.update() #draws anything in while loop on screen variable
    clock.tick(120)