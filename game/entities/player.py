import pygame
from library.common import Events

from game.entities.abc import CollidableEntity, MovingEntity
from game.entities.enums import Entities
from game.common import SCREEN_SIZE
import game.common


class Player(CollidableEntity):
    SIZE = 50, 50
    VEL = 6.0

    def __init__(self) -> None:
        image = pygame.Surface(self.SIZE)
        image.fill("brown")
        super().__init__(
            image=image,
            pos=pygame.Vector2(SCREEN_SIZE[0] - 100, SCREEN_SIZE[1] // 2),
            type=Entities.PLAYER,
        )
        self.sign = 1
        self.vel = self.VEL
        self.is_space_pressed = False

    def handle_input(self, events: Events):
        """
        Changes side when space bar is pressed.
        """

        self.is_space_pressed = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.sign *= -1
                    self.is_space_pressed = True

    def predicted_pos(self, dt: float) -> pygame.Vector2:
        pos = self.pos.copy()
        pos.x += self.vel * dt * self.sign * (game.common.UNIVERSAL_SPEEDUP / 10)

        return pos


    def move(self, dv: pygame.Vector2) -> None:
        self.pos += dv 
        self.rect.topleft = self.pos

    def update(self, dt: float):
        self.pos.x += self.vel * dt * self.sign * (game.common.UNIVERSAL_SPEEDUP / 10)
        self.rect.topleft = self.pos

