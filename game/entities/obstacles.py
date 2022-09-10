import pygame

from game.entities.abc import CollidableEntity
import game.common
from library.common import Pos, ColorValue
from game.entities.enums import Entities

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

class Spike(CollidableEntity):
    def __init__(self, height: int, pos: Pos, dir: str) -> None:
        image = _render_triangle(height, "purple", dir)
        super().__init__(image, pos, Entities.SPIKE)
        self.vel = 0.5


    def update(self, dt: float):
        self.pos.y += self.vel * dt * game.common.UNIVERSAL_SPEEDUP
        self.rect.topleft = self.pos


