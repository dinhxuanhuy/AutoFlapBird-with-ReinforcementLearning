import pygame
import sys

import config
from itertools import cycle

playerIndexGen = cycle([0, 1, 2, 1])  # down-mid-up-mid
playerIndex = 0
anim_counter = 0


pygame.init()

def _spawn_pipe_every(frames_until_spawn):
    if frames_until_spawn <= 0:
        config.generate_pipe()
        return 100
    return frames_until_spawn - 1


def     menu():
    """Main menu loop. Shows animated background and four options.
    Returns: one of ("ai play", "people play", "train", "quit")
    """
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("data/assets/audio/nhacnen_1.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    screen = config.window

    options = [
        ("ai play", config.IMAGES["btn_ai"]),
        ("people play", config.IMAGES["btn_human"]),
        ("pva", config.IMAGES["btn_pva"]),
        ("train", config.IMAGES["btn_train"]),
        ("quit", config.IMAGES["btn_quit"]),
    ]

    selected_idx = 0
    pipe_spawn = 10
    running = True

    while running:
        # --- UPDATE BG ELEMENTS ---
        pipe_spawn = _spawn_pipe_every(pipe_spawn)

        # Update pipes (draw later)
        for pipe in list(config.pipes):
            pipe.update()
            if pipe.offscreen:
                try:
                    config.pipes.remove(pipe)
                except ValueError:
                    pass

        # --- DRAW ---
        screen.fill((0, 0, 0))
        config.background.draw(screen)

        # draw pipes
        for pipe in config.pipes:
            pipe.draw(screen)

        # moving ground
        config.ground.draw(screen)
        config.ground.update()

        # title
        if "title" in config.IMAGES:
            title_img = config.IMAGES["title"]
            rect = title_img.get_rect(center=(config.win_width // 2, 50))
            screen.blit(title_img, rect)

            global playerIndex, anim_counter
            anim_counter += 1
            if anim_counter % 3 == 0:  # đổi frame nhanh (mỗi 3 ticks)
                playerIndex = next(playerIndexGen)

            bird_img = config.IMAGES["player_red"][playerIndex]
            bird_rect = bird_img.get_rect(center=(config.win_width // 2, rect.bottom + 30))  # cách title 30px
            screen.blit(bird_img, bird_rect)

        # buttons
        button_rects = []

        start_y = 180
        end_y = config.win_height - 150
        gap = (end_y - start_y) // (len(options) - 1)

        for i, (key, img) in enumerate(options):
            scale = 2.0  # hệ số phóng to
            scaled_img = pygame.transform.scale(
                img,
                (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            rect = scaled_img.get_rect(center=(config.win_width // 2, start_y + i * gap))

            # blit ảnh to
            screen.blit(scaled_img, rect)

            # rect click vẫn lấy theo ảnh gốc
            click_rect = img.get_rect(center=(config.win_width // 2, start_y + i * gap))
            button_rects.append((key, click_rect))

        # draw author logo (bottom-left corner)
        if "author" in config.IMAGES:
            author_img = config.IMAGES["author"]
            rect = author_img.get_rect()
            rect.bottomleft = (10, config.win_height - 10)  # cách lề 10px
            screen.blit(author_img, rect)
        pygame.display.flip()
        clock.tick(config.FPS)



        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEMOTION:
                for i, (key, rect) in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        selected_idx = i

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key, rect in button_rects:
                    if rect.collidepoint(event.pos):
                        try:
                            config.play_sound("swoosh")
                        except Exception:
                            pass
                        return key

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected_idx = (selected_idx - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected_idx = (selected_idx + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    choice = options[selected_idx][0]
                    try:
                        config.play_sound("swoosh")
                    except Exception:
                        pass
                    return choice


menu()