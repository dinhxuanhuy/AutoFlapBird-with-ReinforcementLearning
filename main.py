import sys
import pygame
import config
import menu
from modes import run_ai_play, run_people_play, run_train_info

if __name__ == "__main__":
    while True:
        choice = menu.menu()
        if choice == "quit":
            sys.exit(0)
        elif choice == "ai play":
            config.TRAINING_MODE = config.TrainingMode.AI_PLAY
            pygame.mixer.music.stop()
            run_ai_play()
        elif choice == "people play":
            config.TRAINING_MODE = config.TrainingMode.NORMAL
            pygame.mixer.music.stop()
            run_people_play()
        elif choice == "train":
            pygame.mixer.music.stop()
            run_train_info()
