import pygame
from sys import exit
import config
import components
import population
import player
pygame.init()
bird = player.Player()
clock = pygame.time.Clock()
def generate_pipe():
    config.pipes.append(components.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
def main():
    pipe_spawn_timer = 10
    while True:
        quit_game()
        config.window.fill((0, 0, 0))
        clock.tick(60)
        config.ground.draw(config.window)
        if pipe_spawn_timer <= 0:
            generate_pipe()
            pipe_spawn_timer = 200
        pipe_spawn_timer -= 1
        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)
        if bird.alive:
            #read key inputs if equal space
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                bird.bird_flap()

            bird.draw(config.window)
            bird.update(config.ground)
        pygame.display.flip()


main()