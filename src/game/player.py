import pygame
import pygame_wrapper as pgw


class Player:
    def __init__(self, sx, sy):
        self.x = float(sx)
        self.y = float(sy)
        self.dx = 0
        self.dy = 0

        self.hitbox = pygame.FRect((self.x, self.y), (50, 100))

        self.model = None  # add model later

    def render(self, surf: pygame.Surface, hitbox: bool = False):
        if hitbox:
            pygame.draw.rect(surf, (200, 0, 0), self.hitbox, width=5)

        if self.model is not None:
            surf.blit(self.model, (self.x, self.y))

    def hook_events(self, events, dt):
        # hook events when needed

        keys = pygame.key.get_pressed()
        self.__movement(keys, dt)

    def __movement(self, keys, dt):
        if keys[pygame.K_w]:
            self.dy = 1

        if keys[pygame.K_s]:
            self.dy = -1

        if keys[pygame.K_a]:
            self.dx = -1

        if keys[pygame.K_d]:
            self.dx = 1

        self.x += self.dx
        self.y += self.dy

        if self.dy < 0:
            self.dy += (1 * dt)
            if self.dy >= 0:
                self.dy = 0

        elif self.dy > 0:
            self.dy -= (1 * dt)
            if self.dy <= 0:
                self.dy = 0

        if self.dx < 0:
            self.dx += (1 * dt)
            if self.dx >= 0:
                self.dx = 0

        elif self.dx > 0:
            self.dx -= (1 * dt)
            if self.dx <= 0:
                self.dx = 0

