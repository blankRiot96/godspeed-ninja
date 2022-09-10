import pygame
from library.common import EventInfo, Pos

import game.common
from game.common import SCREEN_SIZE
from game.entities.abc import CollidableEntity
from game.entities.enums import Entities


class Platform(CollidableEntity):
    SPEED = 1.2
    MAX_INCREMENT = 1

    def __init__(self, image: pygame.Surface, pos: Pos, type: Entities) -> None:
        super().__init__(image, pos, type)
        self.alive = True
        self.size = self.image.get_width()
