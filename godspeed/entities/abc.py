import abc
from typing import Optional

import pygame
from pglib.common import Pos, Size
from typing_extensions import Self

from godspeed.common import SCREEN_SIZE
from godspeed.entities.enums import Entities


class Entity(abc.ABC):
    def __init__(self, image: pygame.Surface, pos: Pos, type: Entities) -> None:
        self.image = image
        self.pos = pos
        self.type = type

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.pos)


class CollidableEntity(Entity):
    def __init__(
        self,
        image: pygame.Surface,
        pos: Pos,
        type: Entities,
        size: Optional[Size] = None,
    ) -> None:
        super().__init__(image, pos, type)
        if size:
            self.size = size
        else:
            self.size = self.image.get_size()
        self.rect = pygame.Rect(pos, self.size)
        self.colliding_with = None

    def collides(self, other: Self) -> bool:
        is_colliding = self.rect.colliderect(other.rect)
        if is_colliding:
            self.colliding_with = other.type
        else:
            self.colliding_with = None

        return is_colliding

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)


class MovingEntity(CollidableEntity):
    def __init__(
        self,
        image: pygame.Surface,
        pos: Pos,
        type: Entities,
        size: Optional[Size] = None,
    ) -> None:
        super().__init__(image, pos, type, size)
        self.alive = True

    def update(self):
        if self.pos.y > SCREEN_SIZE[1]:
            self.alive = False
