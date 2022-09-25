from typing import Optional

import pygame
from pglib.common import EventInfo, Pos, Size

import src.common
from src.common import SCREEN_SIZE
from src.entities.abc import MovingEntity
from src.entities.enums import Entities


class Platform(MovingEntity):
    SPEED = 1.2
    MAX_INCREMENT = 1

    def __init__(
        self,
        image: pygame.Surface,
        pos: Pos,
        type: Entities,
        size: Optional[Size] = None,
        special: bool = False,
    ) -> None:
        super().__init__(image, pos, type, size)
        self.is_special = special
        self.vel = 0.3

    def update(self, dt: float):
        dy = self.vel * dt * src.common.UNIVERSAL_SPEEDUP
        if self.is_special:
            self.pos.y += dy
            if self.pos.y >= SCREEN_SIZE[1]:
                self.pos.y = -SCREEN_SIZE[1] + dy
            self.rect.topleft = self.pos
            return

        super().update()
        self.pos.y += dy * 0.9
        self.rect.topleft = self.pos

    def draw(self, screen):
        if self.is_special:
            if self.rect.x < SCREEN_SIZE[0] / 2:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x - 94 + 29, self.rect.y))
        else:
            screen.blit(self.image, self.rect)
