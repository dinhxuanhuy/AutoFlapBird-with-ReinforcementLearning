import sys
import pygame
import config
import menu
from FlappyBird.config import player
from modes import run_ai_play, run_people_play, run_train_info , run_ai_vs_player

if __name__ == "__main__":
    while True:
        choice = menu.menu()
        if choice == "quit":
            sys.exit(0)
        elif choice == "ai play":
            print("You chose AI play")
            config.TRAINING_MODE = config.TrainingMode.AI_PLAY
            pygame.mixer.music.stop()
            run_ai_play()

        elif choice == "pva":
            print("You chose Player vs AI")
            config.TRAINING_MODE = config.TrainingMode.VS
            print(config.TRAINING_MODE)
            if config.player_AI is None:
                config.player_AI = config.create_player_ai()
            pygame.mixer.music.stop()
            run_ai_vs_player()

        elif choice == "people play":
            print("You chose People play")
            config.TRAINING_MODE = config.TrainingMode.NORMAL
            pygame.mixer.music.stop()
            run_people_play()

        elif choice == "train":
            pygame.mixer.music.stop()
            run_train_info()
