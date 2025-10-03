import config
import pygame

from game_loop import GameLoop

def run_ai_vs_player():
    loop = GameLoop()
    loop.reset()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                if not loop.game_over:          # chỉ flap khi còn sống
                    config.Flap = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if loop.game_over:
                    # click nút trên overlay
                    if loop.retry_rect and loop.retry_rect.collidepoint(event.pos):
                        loop.reset()
                    elif loop.home_rect and loop.home_rect.collidepoint(event.pos):
                        return
                else:
                    # click để flap khi đang chơi
                    config.Flap = True

        loop.step()
        loop.render()


def run_ai_play():
    loop = GameLoop()
    loop.reset()
    while True:
        loop.step()
        if loop.game_over:
            loop.reset()
        loop.render()


def run_people_play():
    loop = GameLoop()
    loop.reset()
    while True:
        # CHỈ MỘT event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                if not loop.game_over:          # chỉ flap khi còn sống
                    config.Flap = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if loop.game_over:
                    # click nút trên overlay
                    if loop.retry_rect and loop.retry_rect.collidepoint(event.pos):
                        loop.reset()
                    elif loop.home_rect and loop.home_rect.collidepoint(event.pos):
                        return
                else:
                    # click để flap khi đang chơi
                    config.Flap = True

        loop.step()
        loop.render()


def run_train_info():
    print("\nMD")
    print("Train thường có UI:")
    print("   python main.py --mode train --episodes 1000")
    print("Train không UI (nhanh):")
    print("   python main.py --mode noui --episodes 10000 --fps 60")
    print("AI chơi sau khi train:")
    print("   python main.py --mode ai")
    print("Test nhanh với ít episodes:")
    print("   python main.py --mode noui --episodes 100 --max-score 50\n")
