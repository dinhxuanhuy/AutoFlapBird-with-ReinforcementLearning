import components
import pygame
import random
from player import Player as p
from agent import Agent
# Thêm vào đầu file config.py
import argparse
import sys
Flap = False
# Training modes
class TrainingMode:
    NORMAL = "normal"      # Chơi thường có UI
    TRAIN = "train"        # Train có UI
    TRAIN_NOUI = "noui"    # Train không UI
    AI_PLAY = "ai"         # AI chơi có UI

# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Flappy Bird Q-Learning')
    parser.add_argument('--mode', choices=['normal', 'train', 'noui', 'ai'],
                        default='train', help='Game mode')
    parser.add_argument('--episodes', type=int, default=10000,
                        help='Number of training episodes')
    parser.add_argument('--fps', type=int, default=60,
                        help='Frames per second')
    parser.add_argument('--max-score', type=int, default=1000000,
                        help='Max score per episode')
    return parser.parse_args()

# Global config
args = parse_args()
TRAINING_MODE = args.mode
EPISODES = args.episodes
FPS = args.fps
MAX_SCORE = args.max_score

win_height = 512
win_width = 288
# amount by which base can maximum shift to left
pipegapsize = 100  # gap between upper and lower part of pipe
window = None
if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    window = pygame.display.set_mode((win_width, win_height))


IMAGES={}
BACKGROUNDS_LIST = (
    "data/assets/sprites/background-day.png",
    "data/assets/sprites/background-night.png",
)

randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    IMAGES["background"] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()
else:
    IMAGES["background"] = pygame.image.load(BACKGROUNDS_LIST[randBg])

background = components.Background(win_width, win_height)
if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    background.set_img(IMAGES["background"])



if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    IMAGES["base"] = pygame.transform.scale(
        pygame.image.load("data/assets/sprites/base.png").convert_alpha(),
        (win_width, pygame.image.load("data/assets/sprites/base.png").get_height())
    )
else:
    IMAGES["base"] = pygame.image.load("data/assets/sprites/base.png")

ground = components.Ground(win_width, win_height)
if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    ground.set_img(IMAGES["base"])
if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    IMAGES["pipe"] = pygame.image.load("data/assets/sprites/pipe-green.png").convert_alpha()
else:
    IMAGES["pipe"] = pygame.image.load("data/assets/sprites/pipe-green.png")
pipes= []
IMAGES['player'] =(
        "data/assets/sprites/redbird-upflap.png",
        "data/assets/sprites/redbird-midflap.png",
        "data/assets/sprites/redbird-downflap.png",
        "data/assets/sprites/bluebird-upflap.png",
        "data/assets/sprites/bluebird-midflap.png",
        "data/assets/sprites/bluebird-downflap.png"
)



agent = Agent()

def create_player():
    if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
        return p(win_width, win_height, images=[
            pygame.image.load(IMAGES['player'][0]).convert_alpha(),
            pygame.image.load(IMAGES['player'][1]).convert_alpha(),
            pygame.image.load(IMAGES['player'][2]).convert_alpha(),
        ])
    else:
        return p(win_width, win_height, images=None )

def create_player2():
    if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
        return p(win_width, win_height, images=[
            pygame.image.load(IMAGES['player'][3]).convert_alpha(),
            pygame.image.load(IMAGES['player'][4]).convert_alpha(),
            pygame.image.load(IMAGES['player'][5]).convert_alpha(),
        ])
    else:
        return p(win_width, win_height, images=None )

player = create_player()

player2 = create_player2()


def generate_pipe():
    pipe = components.Pipe(win_width, win_height, img=IMAGES["pipe"], gap_size=pipegapsize)
    pipes.append(pipe)