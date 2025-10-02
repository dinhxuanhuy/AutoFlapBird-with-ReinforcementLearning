import pygame
from sys import exit
import config
import components
import random

# Chỉ khởi tạo pygame khi cần UI4
print(f"Training mode: {config.TRAINING_MODE}")
if config.TRAINING_MODE != config.TrainingMode.TRAIN_NOUI:
    pygame.init()
    clock = pygame.time.Clock()
else:
    # Train không UI: chỉ cần time tracking
    import time

    start_time = time.time()


def quit_game():
    if config.TRAINING_MODE != config.TrainingMode.TRAIN_NOUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if config.TRAINING_MODE != config.TrainingMode.NORMAL:
                    config.agent.terminate_game(alive=False)
                    print("Q-values saved.")
                pygame.quit()
                exit()
            if config.TRAINING_MODE == config.TrainingMode.NORMAL or config.TRAINING_MODE == config.TrainingMode.TRAIN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        config.Flap = True


def main():
    pipe_spawn_time = 10
    episode_count = 0 

    while True:
        # Train không UI: bỏ qua xử lý events
        quit_game()
        if config.TRAINING_MODE != config.TrainingMode.TRAIN_NOUI:

            config.window.fill((0, 0, 0))
            config.background.draw(config.window)
        # Game logic (luôn chạy)
        if pipe_spawn_time <= 0:
            config.generate_pipe()
            pipe_spawn_time = 100
        pipe_spawn_time -= 1

        # Update pipes
        for pipe in config.pipes:
            if config.TRAINING_MODE != config.TrainingMode.TRAIN_NOUI:
                pipe.draw(config.window)
            pipe.update()
            if pipe.offscreen:
                config.pipes.remove(pipe)

        # Player logic

        if config.player.alive:
            if config.TRAINING_MODE != config.TrainingMode.NORMAL:
                config.player.think()  # AI hành động
            else :
                if config.Flap:
                    config.player.flap()
                    config.Flap = False
            config.player.update()
            if config.TRAINING_MODE != config.TrainingMode.TRAIN_NOUI:
                config.player.draw(config.window)
        else:
            episode_count += 1
            print(f"Episode {episode_count}: Score {config.player.score}")
            config.agent.update_scores(died=True, printLogs=True)
            if config.TRAINING_MODE != config.TrainingMode.NORMAL:
                config.agent.record_score(config.player.get_score())
            # Reset game

            config.pipes = []
            pipe_spawn_time = 10
            config.player = config.create_player()

            # Kiểm tra điều kiện dừng
            if config.TRAINING_MODE == config.TrainingMode.TRAIN_NOUI:
                if episode_count >= config.EPISODES:
                    print(f"Training completed after {episode_count} episodes")
                    config.agent.terminate_game()
                    exit()
        
        if config.player2.alive:
            if config.Flap:
                config.player2.flap()
                config.Flap = False
            config.player2.update()
            
            if config.TRAINING_MODE != config.TrainingMode.TRAIN_NOUI:
                config.player2.draw(config.window)
        else:
            print("Player died. AI Wins!")
            pygame.quit()
            exit()

        # Kiểm tra va chạm với ống cho cả hai người chơi
        
        
        # Rendering (chỉ khi có UI)
        if config.TRAINING_MODE != config.TrainingMode.TRAIN_NOUI:
            config.ground.draw(config.window)
            config.ground.update()
            pygame.display.flip()
            clock.tick(30)
        else:
            # Train không UI: tối ưu tốc độ
            if episode_count % 500 == 0 and episode_count > 0 and (not config.player.alive):
                elapsed = time.time() - start_time
                print(f"Episode {episode_count}, Time elapsed: {elapsed:.2f} seconds")
                config.agent.dump_qvalues(force=True)

            pass


if __name__ == "__main__":
    main()
