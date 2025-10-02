import pygame
import random

class Ground:
    def __init__(self, win_width, win_height, img=None, scroll_speed=4):
        self.win_width = int(win_width)
        self.win_height = int(win_height)
        self.img = img
        if img:
            self.base_width = img.get_width()
            self.base_height = img.get_height()
        else:
            self.base_width = 336
            self.base_height = 112

        # top y của base (BASEY giống code gốc)
        self.base_y = int(self.win_height * 0.79)

        # two offsets for seamless tiling
        self.basex1 = 0
        self.basex2 = self.base_width

        self.scroll_speed = scroll_speed

        # collision band (thin rect at top of base)
        self.collision_rect = pygame.Rect(0, self.base_y, self.win_width, 5)

    def ground_level(self):
        return self.base_y

    def update(self, dt=None):
        """Nếu dt không None thì coi scroll_speed là px/sec, ngược lại coi là px/frame."""
        if dt is not None:
            dx = self.scroll_speed * dt
        else:
            dx = self.scroll_speed

        self.basex1 -= dx
        self.basex2 -= dx

        # wrap: khi một bản off-screen sang trái, đặt nó ở bên phải bản kia
        if self.basex1 <= -self.base_width:
            self.basex1 = self.basex2 + self.base_width
        if self.basex2 <= -self.base_width:
            self.basex2 = self.basex1 + self.base_width

        # update collision rect
        self.collision_rect.x = 0
        self.collision_rect.y = int(self.base_y)

    def draw(self, window):
        if self.img:
            window.blit(self.img, (int(self.basex1), int(self.base_y)))
            window.blit(self.img, (int(self.basex2), int(self.base_y)))
        else:
            pygame.draw.rect(window, (139,69,19),
                             (int(self.basex1), int(self.base_y), self.base_width, self.base_height))
            pygame.draw.rect(window, (139,69,19),
                             (int(self.basex2), int(self.base_y), self.base_width, self.base_height))

    def collides(self, player_rect):
        return player_rect.colliderect(self.collision_rect)

    def set_img(self, img):
        self.img = img
        if img:
            self.base_width = img.get_width()
            self.base_height = img.get_height()
        self.basex2 = self.basex1 + self.base_width
import pygame, random

class Pipe:
    def __init__(self, win_width, win_height, img=None, gap_size=100, speed=4):
        self.win_width = win_width
        self.win_height = win_height
        self.gap_size = gap_size
        self.speed = speed
        self.img = img

        # BASEY = 79% chiều cao màn hình
        self.baseY = int(win_height * 0.79)

        # random vị trí lỗ hổng (gapY)
        self.gapY = random.randrange(0, int(self.baseY * 0.6 - self.gap_size))
        self.gapY += int(self.baseY * 0.2) # cạnh trên của lỗ hổng

        # nếu có ảnh thì lấy kích thước
        if img:
            self.pipe_width = img.get_width()
            self.pipe_height = img.get_height()
        else:
            self.pipe_width = 52   # default Flappy Bird pipe
            self.pipe_height = 320

        # tọa độ x ban đầu của pipe
        self.x = win_width + 10

        # tạo rect cho pipe trên và dưới
        self.top_rect = pygame.Rect(self.x, self.gapY - self.pipe_height, self.pipe_width, self.pipe_height)
        self.bottom_rect = pygame.Rect(self.x, self.gapY + self.gap_size, self.pipe_width, self.baseY - (self.gapY + self.gap_size))
        self.offscreen = False  # cờ để đánh dấu pipe

    def update(self):
        """Di chuyển pipe sang trái"""
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        if self.x < -self.pipe_width:
            self.offscreen = True

    def draw(self, window):
        if self.img:
            # top pipe: vẽ full (đã cache flipped nếu muốn)
            top_img = pygame.transform.flip(self.img, False, True)
            window.blit(top_img, (int(self.top_rect.x), int(self.top_rect.y)))

            # bottom pipe: chỉ vẽ phần từ đầu ảnh xuống visible_h
            visible_h = int(self.bottom_rect.height)
            if visible_h > 0:
                # đảm bảo visible_h không vượt quá self.pipe_height
                visible_h = min(visible_h, self.pipe_height)

                # lấy phần trên cùng của ảnh pipe (từ y=0 tới visible_h)
                src_rect = pygame.Rect(0, 0, self.pipe_width, visible_h)
                portion = self.img.subsurface(src_rect)

                # vẽ phần đó đúng tại vị trí đỉnh ống dưới
                window.blit(portion, (int(self.bottom_rect.x), int(self.bottom_rect.y)))
        else:
            # fallback vẽ full rects (đã đúng trước)
            pygame.draw.rect(window, (0, 255, 0), self.top_rect)
            pygame.draw.rect(window, (0, 255, 0), self.bottom_rect)


class Background:
    def __init__(self, win_width, win_height, img=None, mode="scale"):
        """
        mode: "scale" (stretch to window), "tile" (repeat image), or "center" (draw once center).
        """
        self.win_width = win_width
        self.win_height = win_height
        self.img = img
        self.mode = mode

    def set_img(self, img):
        self.img = img

    def draw(self, window):
        if not self.img:
            window.fill((135,206,250))
            return

        if self.mode == "scale":
            # scale background to fill window
            if (self.img.get_width(), self.img.get_height()) != (self.win_width, self.win_height):
                scaled = pygame.transform.scale(self.img, (self.win_width, self.win_height))
                window.blit(scaled, (0,0))
            else:
                window.blit(self.img, (0,0))

        elif self.mode == "tile":
            # tile the background to cover whole window
            iw, ih = self.img.get_width(), self.img.get_height()
            for x in range(0, self.win_width, iw):
                for y in range(0, self.win_height, ih):
                    window.blit(self.img, (x,y))

        elif self.mode == "center":
            # draw once at top-left (original behavior) but center vertically/horizontally
            x = (self.win_width - self.img.get_width()) // 2
            y = (self.win_height - self.img.get_height()) // 2
            window.fill((0,0,0))
            window.blit(self.img, (x,y))
        else:
            window.blit(self.img, (0,0))