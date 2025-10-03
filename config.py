import components
import pygame
import random
from player import Player as p
from agent import Agent
# Thêm vào đầu file config.py
import argparse
import sys

import os
# Training modes
class TrainingMode:
    NORMAL = "normal"      # Chơi thường có UI
    TRAIN = "train"        # Train có UI
    VS = "pva"         # AI vs Player
    TRAIN_NOUI = "noui"    # Train không UI
    AI_PLAY = "ai"         # AI chơi có UI


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

"""win_height = 512
win_width = 288"""
win_height = 512
win_width = 288
# amount by which base can maximum shift to left
pipegapsize = 100
window = None
if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    pygame.init()
    window = pygame.display.set_mode((win_width, win_height))

IMAGES = {}

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
        (win_width, pygame.image.load("data/assets/sprites/base.png").get_height()))
else:
    IMAGES["base"] = pygame.image.load("data/assets/sprites/base.png")

ground = components.Ground(win_width, win_height)
if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    ground.set_img(IMAGES["base"])
# Pipe image (single texture; components.Pipe draws top flipped)
if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    IMAGES["pipe"] = pygame.image.load("data/assets/sprites/pipe-green.png").convert_alpha()
else:
    IMAGES["pipe"] = pygame.image.load("data/assets/sprites/pipe-green.png")
pipes = []
IMAGES['player_red'] = [
    pygame.image.load("data/assets/sprites/redbird-upflap.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/redbird-midflap.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/redbird-downflap.png").convert_alpha()
]
IMAGES['player_blue'] = [
    pygame.image.load("data/assets/sprites/bluebird-upflap.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/bluebird-midflap.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/bluebird-downflap.png").convert_alpha(),
]
agent = Agent()

def create_player():
    """Instantiate Player with loaded sprites (in UI) or None (noui)."""
    from player import Player  # local import to avoid circular dependency
    if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
        return Player(win_width, win_height, images=IMAGES['player_red'])
    else:
        return Player(win_width, win_height, images=None)
def create_player_ai():
    """Instantiate Player with loaded sprites (in UI) or None (noui)."""
    from player import Player  # local import to avoid circular dependency
    if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
        return Player(win_width, win_height, images=IMAGES['player_blue'])
    else:
        return Player(win_width, win_height, images=None)


player = create_player() # AI player
player_AI = None
if TRAINING_MODE == TrainingMode.VS:
    player_AI = create_player_ai() # AI player



def generate_pipe():
    speed = 4 if TRAINING_MODE == TrainingMode.NORMAL else 4




    pipe = components.Pipe(win_width, win_height, img=IMAGES["pipe"], gap_size=100, speed=speed)
    pipes.append(pipe)
# Input latch for human flap in NORMAL mode
Flap = False

#PHAN THEM VAO #######THINH################
#AM THANH
SOUNDS = {}

if TRAINING_MODE != TrainingMode.TRAIN_NOUI:
    pygame.mixer.init()
    # Bật nhạc nền
    try:
        pygame.mixer.music.load("data/assets/audio/nhacnen_1.wav")
        pygame.mixer.music.set_volume(0.5)  # âm lượng 0.0 -> 1.0
        pygame.mixer.music.play(-1)         # -1 = lặp vô hạn
    except Exception as e:
        print("Không mở được nhạc nền:", e)

    soundExt = ".wav" if "win" in sys.platform.lower() else ".ogg"

    def _load_sound(name):
        return pygame.mixer.Sound(f"data/assets/audio/{name}{soundExt}")

    SOUNDS["die"] = _load_sound("die")
    SOUNDS["hit"] = _load_sound("hit")
    SOUNDS["point"] = _load_sound("point")
    SOUNDS["swoosh"] = _load_sound("swoosh")
    SOUNDS["wing"] = _load_sound("wing")







def play_sound(key: str):
    if TRAINING_MODE == TrainingMode.TRAIN_NOUI:
        return
    snd = SOUNDS.get(key)
    if snd:
        snd.play()
#ANH
IMAGES["numbers"] = [
    pygame.image.load("data/assets/sprites/0.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/1.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/2.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/3.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/4.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/5.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/6.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/7.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/8.png").convert_alpha(),
    pygame.image.load("data/assets/sprites/9.png").convert_alpha(),
]


def draw_score(surface, score: int, y: int = 40):
    if TRAINING_MODE == TrainingMode.TRAIN_NOUI:
        return

    digits = list(str(score))
    num_images = [IMAGES["numbers"][int(d)] for d in digits]

    total_width = sum(img.get_width() for img in num_images)
    start_x = (win_width - total_width) // 2
    for img in num_images:
        surface.blit(img, (start_x, y))
        start_x += img.get_width()



##GIA VI
IMAGES["title"] = pygame.image.load("data/assets/sprites/title.png").convert_alpha()
IMAGES["gameover"] = pygame.image.load("data/assets/sprites/gameover.png").convert_alpha()
IMAGES["score_panel"] = pygame.image.load("data/assets/sprites/score_panel.png").convert_alpha()
IMAGES["button_retry"] = pygame.image.load("data/assets/sprites/button_retry.png").convert_alpha()
IMAGES["button_home"] = pygame.image.load("data/assets/sprites/button_homet.png").convert_alpha()


IMAGES["btn_ai"] = pygame.image.load("data/assets/sprites/AI_Play.png").convert_alpha()
IMAGES["btn_human"] = pygame.image.load("data/assets/sprites/Human_Play.png").convert_alpha()
IMAGES["btn_train"] = pygame.image.load("data/assets/sprites/Train.png").convert_alpha()
IMAGES["btn_quit"] = pygame.image.load("data/assets/sprites/Quit.png").convert_alpha()


IMAGES["author"] = pygame.image.load("data/assets/sprites/author.png").convert_alpha()

IMAGES["btn_pva"] = pygame.image.load("data/assets/sprites/P_V_A.png").convert_alpha()
