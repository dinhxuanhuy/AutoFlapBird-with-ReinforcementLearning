import pygame
import config


class UIOverlay:
    def draw_game_over(self):
        overlay = pygame.Surface((config.win_width, config.win_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        config.window.blit(overlay, (0, 0))

        go_img = config.IMAGES["gameover"]
        go_rect = go_img.get_rect(center=(config.win_width // 2, 150))
        config.window.blit(go_img, go_rect)

        panel = config.IMAGES["score_panel"]
        panel_rect = panel.get_rect(center=(config.win_width // 2, 260))
        config.window.blit(panel, panel_rect)

        # Score bằng ảnh số
        digits = list(str(config.player.get_score()))
        num_images = [config.IMAGES["numbers"][int(d)] for d in digits]
        total_width = sum(img.get_width() for img in num_images)
        start_x = panel_rect.right - total_width - 40
        y = panel_rect.top + 60
        for img in num_images:
            config.window.blit(img, (start_x, y))
            start_x += img.get_width()

        retry_img = config.IMAGES["button_retry"]
        retry_rect = retry_img.get_rect(center=(config.win_width // 2 - 60, 360))
        config.window.blit(retry_img, retry_rect)

        home_img = config.IMAGES["button_home"]
        home_rect = home_img.get_rect(center=(config.win_width // 2 + 60, 360))
        config.window.blit(home_img, home_rect)

        return retry_rect, home_rect
