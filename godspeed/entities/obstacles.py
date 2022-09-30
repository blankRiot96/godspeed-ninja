import pygame
from pglib.common import ColorValue, Pos

import godspeed.common
from godspeed.entities.abc import MovingEntity
from godspeed.entities.enums import Entities


def _render_triangle(height: int, color: ColorValue, dir: str) -> pygame.Surface:
    surf = pygame.Surface((height, height), pygame.SRCALPHA)
    r = surf.get_rect()
    # verticies of the triangle are A, B, and C.
    a = (r.width // 2, 0)
    b = (0, r.height)
    c = (r.width, r.height)
    pygame.draw.polygon(surf, color, (a, b, c))

    if dir == "right":
        surf = pygame.transform.rotate(surf, 90)
    elif dir == "left":
        surf = pygame.transform.rotate(surf, -90)
    return surf


class Spike(MovingEntity):
    def __init__(self, height: int, pos: Pos, dir: str) -> None:
        self.height = height
        self.dir = dir 
        super().__init__(self.gen_image(), pos, Entities.SPIKE)
        self.vel = 0.5

    def gen_image(self) -> pygame.Surface:
        s = 1 if self.dir == "right" else -1
        image = _render_triangle(self.height + 10, "black", self.dir)
        fore_image = pygame.transform.scale(godspeed.common.assets["spike"], (self.height, self.height))
        if self.dir == "right":
            fore_image = pygame.transform.rotate(fore_image, 90)
        elif self.dir == "left":
            fore_image = pygame.transform.rotate(fore_image, -90)
        else:
            raise ValueError("Invalid value given for Spike.dir, should be right or left.")
        
        r = image.get_rect()
        image.blit(fore_image, fore_image.get_rect(center=(r.centerx + (2 * s), r.centery)))
        return image 


    def update(self, dt: float):
        super().update()
        self.pos.y += self.vel * dt * godspeed.common.UNIVERSAL_SPEEDUP
        self.rect.topleft = self.pos


class Shuriken(MovingEntity):
    SIZE = 32
    ROTAT_SPEED = 1.2
    SPEED = 1.2
    once = True

    def __init__(self, pos: Pos) -> None:
        if self.once:
            Shuriken.ORIGINAL_IMAGE = godspeed.common.assets["shuriken"].copy()
            self.once = False
        super().__init__(Shuriken.ORIGINAL_IMAGE.copy(), pos, Entities.SHURIKEN)
        self.angle = 0
        self.original_rect = self.ORIGINAL_IMAGE.get_rect()

    def update(self, dt: float):
        super().update()
        self.angle += self.ROTAT_SPEED * dt
        self.pos.y += self.SPEED * dt
        self.original_rect.topleft = self.pos
        self.rect = self.image.get_rect(center=self.original_rect.center)
        self.image = pygame.transform.rotate(self.ORIGINAL_IMAGE, self.angle)
        self.angle %= 360
