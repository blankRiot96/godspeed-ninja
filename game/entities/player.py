import pygame

from game.entities.abc import CollidableEntity


class Player(CollidableEntity):
    SIZE = 50, 50

    def __init__(self) -> None:
        super().__init__(image=pygame.Surface(self.SIZE), pos=pygame.Vector2(0, 0))

    def update(self):
        pass
