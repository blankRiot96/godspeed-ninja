import pygame
from library.common import EventInfo, Pos

from game.common import SCORE, SCREEN_SIZE
from game.entities.abc import CollidableEntity
from game.entities.enums import Entities


class Platform(CollidableEntity):
    SPEED = 1.2

    def __init__(self, image: pygame.Surface, pos: Pos, type: Entities) -> None:
        super().__init__(image, pos, type)
        self.alive = True

    def update(self, event_info: EventInfo):
        self.pos.y += (event_info["dt"] * self.SPEED) + (SCORE / 10)

        if self.pos.y > SCREEN_SIZE[1]:
            self.alive = False
