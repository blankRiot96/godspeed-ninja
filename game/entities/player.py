import pygame

from typing_extensions import Self

from pglib.common import Events

import game.common
from game.common import SCREEN_SIZE
from game.entities.abc import CollidableEntity, MovingEntity
from game.entities.enums import Entities


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

        if self.colliding_with is None:
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


    def predicted_move(self, dt: float) -> pygame.Vector2:
        dx = self.vel * dt * self.sign * (game.common.UNIVERSAL_SPEEDUP / 10)

        return pygame.Vector2(dx, 0) 

    def would_collide(self, other: MovingEntity, dt: float) -> bool:
        rect = self.move_rect(self.predicted_move(dt))
        is_colliding = rect.colliderect(other.rect)
        if is_colliding:
            self.colliding_with = other.type
        else:
            self.colliding_with = None

        return is_colliding

    # def collides(self, other: MovingEntity, dt: float) -> bool:
    #     predicted_pos = self.predicted_pos(dt)
    #     predicted_rect = pygame.Rect(predicted_pos, self.SIZE)
    #     is_colliding = predicted_rect.colliderect(other.rect)
    #     if is_colliding:
    #         self.colliding_with = other.type
    #     else:
    #         self.colliding_with = None

    #     return is_colliding, predicted_pos

    def move_rect(self, dv: pygame.Vector2) -> None:
        stub = self.rect.copy()
        pos = self.pos.copy()
        pos += dv 
        stub.topleft = pos 

        return stub


    def move_ip(self, dv: pygame.Vector2) -> None:
        self.pos += dv
        self.rect.topleft = self.pos

    def update(self, dt: float):
        self.pos.x += self.vel * dt * self.sign * (game.common.UNIVERSAL_SPEEDUP / 10)
        self.rect.topleft = self.pos

