import pygame
from sys import exit
import config
import components
import random



pygame.init()
clock = pygame.time.Clock()

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.agent.terminate_game()
            pygame.quit()
            exit()
def main():
    pipe_spawn_time = 10
    while True:
        quit_game()
        config.window.fill((0, 0, 0))
        config.background.draw(config.window)
        clock.tick(60)

        # spawn pipe
        if pipe_spawn_time == 0:
            config.generate_pipe()
            pipe_spawn_time = 100
        pipe_spawn_time -= 1

        # update & draw pipes
        for pipe in config.pipes:
            pipe.draw(config.window)
            pipe.update()
            if pipe.offscreen:
                config.pipes.remove(pipe)

        # autoplay: cho agent quyết định
        if config.player.alive:
            config.player.think()   # AI hành động (flap hay không)
            config.player.update()
            config.player.draw(config.window)
        else:
            # game over -> cập nhật Q-learning
            print("Score:", config.player.score)
            config.agent.update_scores(died=True, printLogs=True)
            # reset
            config.pipes = []
            pipe_spawn_time = 10
            config.player = config.create_player()

        # draw ground
        config.ground.draw(config.window)
        config.ground.update()

        pygame.display.flip()

main()
