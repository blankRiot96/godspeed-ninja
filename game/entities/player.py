import pygame
from library.common import EventInfo

from game.entities.abc import CollidableEntity
from game.entities.enums import Entities


class Player(CollidableEntity):
    SIZE = 50, 50

    def __init__(self) -> None:
        super().__init__(
            image=pygame.Surface(self.SIZE),
            pos=pygame.Vector2(50, 0),
            type=Entities.PLAYER,
        )

    def update(self, event_info: EventInfo):
        pass
