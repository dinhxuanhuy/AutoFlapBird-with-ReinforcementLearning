import components
import pygame
import random
from player import Player as p
from agent import Agent

win_height = 512
win_width = 288
# amount by which base can maximum shift to left
pipegapsize = 100  # gap between upper and lower part of pipe
window = pygame.display.set_mode((win_width, win_height))

IMAGES={}
BACKGROUNDS_LIST = (
    "data/assets/sprites/background-day.png",
    "data/assets/sprites/background-night.png",
)

randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
IMAGES["background"] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

background = components.Background(win_width, win_height)
background.set_img(IMAGES["background"])



IMAGES["base"] = pygame.transform.scale(
    pygame.image.load("data/assets/sprites/base.png").convert_alpha(),
    (win_width, pygame.image.load("data/assets/sprites/base.png").get_height())
)
ground = components.Ground(win_width, win_height)
ground.set_img(IMAGES["base"])
IMAGES["pipe"] = pygame.image.load("data/assets/sprites/pipe-green.png").convert_alpha()
pipes= []
IMAGES['player'] =(
        "data/assets/sprites/redbird-upflap.png",
        "data/assets/sprites/redbird-midflap.png",
        "data/assets/sprites/redbird-downflap.png",
)
agent = Agent()

def create_player():
    return p(win_width, win_height, images=[
        pygame.image.load(IMAGES['player'][0]).convert_alpha(),
        pygame.image.load(IMAGES['player'][1]).convert_alpha(),
        pygame.image.load(IMAGES['player'][2]).convert_alpha(),
    ])

player = create_player()


def generate_pipe():
    pipe = components.Pipe(win_width, win_height, img=IMAGES["pipe"], gap_size=pipegapsize)
    pipes.append(pipe)