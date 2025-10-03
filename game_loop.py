import pygame
import time
import config
from ui import UIOverlay


class GameLoop:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.episode_count = 0
        self.game_over = False
        self.death_sounds_played = False
        self.pipe_spawn_time = 10
        self.start_time = time.time() if config.TRAINING_MODE == config.TrainingMode.TRAIN_NOUI else None
        self.ui_overlay = UIOverlay()

    def reset(self):
        config.pipes = []
        self.pipe_spawn_time = 10
        config.player = config.create_player()
        self.game_over = False
        self.death_sounds_played = False

    def step(self):
        # Spawn pipes
        if self.pipe_spawn_time <= 0:
            config.generate_pipe()
            self.pipe_spawn_time = 100
        self.pipe_spawn_time -= 1

        # Update pipes
        for pipe in list(config.pipes):
            pipe.update()
            if pipe.offscreen:
                config.pipes.remove(pipe)

        # Player update
        if config.player.alive:
            if config.TRAINING_MODE != config.TrainingMode.NORMAL:
                config.player.think()
            else:
                if config.Flap:
                    config.player.flap()
                    config.Flap = False
            config.player.update()
        else:
            # chết
            self.game_over = True
            self.episode_count += 1
            if config.TRAINING_MODE == config.TrainingMode.AI_PLAY:
                print(f"Episode {self.episode_count}: Score {config.player.score}")
            config.agent.update_scores(died=True, printLogs=True)
            if config.TRAINING_MODE != config.TrainingMode.NORMAL:
                config.agent.record_score(config.player.get_score())

    def render(self):
        if config.TRAINING_MODE == config.TrainingMode.TRAIN_NOUI:
            return

        config.window.fill((0, 0, 0))
        config.background.draw(config.window)
        for pipe in config.pipes:
            pipe.draw(config.window)
        config.ground.draw(config.window)
        config.ground.update()

        config.player.draw(config.window)

        config.draw_score(config.window, config.player.get_score())

        if self.game_over and config.TRAINING_MODE == config.TrainingMode.NORMAL:
            self.retry_rect, self.home_rect = self.ui_overlay.draw_game_over()
        else:
            self.retry_rect, self.home_rect = None, None

        pygame.display.flip()
        self.clock.tick(config.FPS)

