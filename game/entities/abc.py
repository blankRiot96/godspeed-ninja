import pygame 
import abc 
from library.common import Pos 
from typing_extensions import Self
from game.entities.enums import Entities


class Entity(abc.ABC):
    def __init__(self, image: pygame.Surface, pos: Pos, type: Entities) -> None:
        self.image = image 
        self.pos = pos 
        self.type = type

class CollidableEntity(Entity):
    def __init__(self, image: pygame.Surface, pos: Pos) -> None:
        super().__init__(image, pos)
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.colliding_with = None

    def collides(self, other: Self) -> bool:
        is_colliding = self.rect.colliderect(other.rect)
        if is_colliding:
            self.colliding_with = other.type 
        else:
            self.colliding_with = None 
        
        return is_colliding

