import pygame
from library.common import EventInfo, Pos

import game.common
from game.common import SCREEN_SIZE
from game.entities.abc import MovingEntity
from game.entities.enums import Entities


class Platform(MovingEntity):
    SPEED = 1.2
    MAX_INCREMENT = 1

    def __init__(
        self, image: pygame.Surface, pos: Pos, type: Entities, special: bool = False
    ) -> None:
        super().__init__(image, pos, type)
        self.is_special = special
        self.size = self.image.get_width()
        self.vel = 0.3

    def update(self, dt: float):
        if not self.is_special:
            super().update()
        self.pos.y += self.vel * dt * game.common.UNIVERSAL_SPEEDUP * 0.9
        self.rect.topleft = self.pos
