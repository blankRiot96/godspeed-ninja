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
        self.spawned_from = False
        self.increment = 0

    def update(self, event_info: EventInfo):
        if self.increment < self.MAX_INCREMENT:
            self.increment = game.common.SCORE / 10
        else:
            print(self.increment)
    
        self.pos.y += (event_info["dt"] * (self.SPEED + self.increment))
        self.rect.topleft = self.pos

        if self.pos.y > SCREEN_SIZE[1]:
            self.alive = False
