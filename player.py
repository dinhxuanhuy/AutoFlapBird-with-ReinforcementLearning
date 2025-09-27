import pygame
from itertools import cycle
import components
import random
import config
from agent import Agent
base_y = int(512* 0.79)
class Player:
    """
    Player class mô phỏng hành vi vật lý của mono code Flappy Bird.
    Sử dụng:
        p = Player(screen_width, screen_height, images=IMAGES['player'])
        p.flap()  # khi cần nhảy
        p.update(dt=None)  # dt: seconds (nếu bạn dùng dt-based), hoặc None để dùng px/frame
        p.draw(window)
        p.get_rect() -> pygame.Rect cho kiểm tra va chạm
    """

    def __init__(
        self,
        win_width,
        win_height,
        images=None,         # tuple of 3 pygame.Surface (up, mid, down)
        x_ratio=0.2,         # playerx = win_width * x_ratio
        start_y=None
    ):
        self.win_w = win_width
        self.win_h = win_height

        # vị trí
        self.x = int(self.win_w * x_ratio)
        self.y = int((self.win_h - (images[0].get_height() if images else 24)) / 2) if start_y is None else int(start_y)

        # images (frames) - nếu không có, dùng None và vẽ rect fallback
        self.images = images
        self.playerIndexGen = cycle([0, 1, 2, 1])
        self.playerIndex = 0
        self.anim_counter = 0   # để đổi frame mỗi vài bước

        # physics (giống mono code)

        self.playerVelY    = - 9  # initial vel (mono dùng -9)
        self.playerMaxVelY = 10   # max downward speed
        self.playerMinVelY = -8   # max upward speed (cap)
        self.playerAccY    = 1    # gravity (per frame or per second if dt)
        self.playerFlapAcc = -9   # velocity when flap
        self.playerFlapped = False
        # trạng thái
        self.alive = True


        # cache width/height (dùng image nếu có)
        if self.images:
            self.width = self.images[0].get_width()
            self.height = self.images[0].get_height()
        else:
            self.width = 34
            self.height = 24
        self.brain = config.agent
        self.score = 0
        self.pipe_passed = None

    # gọi khi muốn chim flap
    def flap(self):
        if not self.playerFlapped and not self.sky_collision():
            self.playerVelY = self.playerFlapAcc
            self.playerFlapped = True

    def think(self):
        if not self.brain:
            return
        next_pipe = None
        for pipe in config.pipes:
            if pipe.x + pipe.pipe_width >= self.x:
                next_pipe = pipe
                break
        # Gọi agent.act(...) với thông tin hiện tại
        action = self.brain.act(self.x, self.y, self.playerVelY, next_pipe)

        if action == 1:
            self.flap()

    def sky_collision(self):
        # check bird hitting top of screen (mono uses playery + h <= 0)
        return self.y < 0
    def ground_collision(self):
        base_y = int(self.win_h * 0.79)
        return self.y + self.height >= base_y
    def pipe_collision(self, pipes):
        """Kiểm tra va chạm rect với list pipe objects (Pipe.collides_with(...) hoặc pipe.rects)."""
        play_rect = self.get_rect()
        for pipe in pipes:
            # nếu pipe cung cấp method collides_with(player_rect), dùng nó
            if hasattr(pipe, "collides_with"):
                if pipe.collides_with(play_rect):
                    return True
            else:
                # fallback: so sánh với top_rect và bottom_rect nếu có
                if play_rect.colliderect(getattr(pipe, "top_rect", pygame.Rect(0,0,0,0))):
                    return True
                if play_rect.colliderect(getattr(pipe, "bottom_rect", pygame.Rect(0,0,0,0))):
                    return True
        return False

    def apply_gravity(self, dt=None):
        if dt is None:
            if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
                self.playerVelY += self.playerAccY # tăng độ cao theo gia tốc (acc)
        else:
            # nếu dùng dt (px/sec), convert acc (treat playerAccY as px/sec^2)
            self.playerVelY += self.playerAccY * dt # px/sec
            if self.playerVelY > self.playerMaxVelY:
                self.playerVelY = self.playerMaxVelY
        try:
            if self.x > config.pipes[0].x + config.pipes[0].pipe_width and not self.pipe_collision(config.pipes) and config.pipes[0] != self.pipe_passed:
                self.pipe_passed = config.pipes[0]
                self.score += 1
        except:
            pass


    def get_score(self):
        return self.score
    def update(self, base_y=None, dt=None):
        """
        Cập nhật trạng thái:
          - base_y: vị trí top-of-base (BASEY). Nếu None, dùng win_h*0.79.
          - dt: seconds since last frame (nếu dùng dt-based). Nếu None dùng px/frame style.
        """
        if base_y is None:
            base_y = int(self.win_h * 0.79)

        # gravity
        self.apply_gravity(dt)
        if self.ground_collision() or self.sky_collision() or self.pipe_collision(config.pipes):
            self.alive = False
            self.playerVelY = 0
            self.y = 0
        # reset flap flag after applying immediate flap
        if self.playerFlapped:
            self.playerFlapped = False

        # cập nhật y; phân biệt dt mode và frame mode
        if dt is None:
            # mono-like: dùng giá trị velocity đơn vị px/frame
            # min(...) để không vượt qua base
            max_step = base_y - self.y - self.height
            self.y = self.y + min(self.playerVelY, max_step)
        else:
            # dt-based (treat velocity as px/sec, so position += vel * dt)
            # ensure we don't pass base
            dy = self.playerVelY * dt
            if self.y + dy + self.height >= base_y:
                self.y = base_y - self.height
            else:
                self.y += dy

        # animation (next frame every 3 updates)
        self.anim_counter += 1
        if self.anim_counter % 3 == 0:
            self.playerIndex = next(self.playerIndexGen)

    def draw(self, window):
        if self.images:
            frame = self.images[self.playerIndex]
            window.blit(frame, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(window, (255, 255, 0), (int(self.x), int(self.y), self.width, self.height))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

