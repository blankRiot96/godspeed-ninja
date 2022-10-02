from typing import Optional
from dataclasses import dataclass

import enum

import pygame
from pglib.common import EventInfo, Pos, Size

import godspeed.common
from godspeed.common import SCREEN_SIZE, PLAT_WIDTH
from godspeed.entities.abc import MovingEntity
from godspeed.entities.enums import Entities


class Platform(MovingEntity):
    SPEED = 1.2
    MAX_INCREMENT = 1

    def __init__(
        self,
        image: pygame.Surface,
        pos: Pos,
        type: Entities,
        size: Optional[Size] = None,
        special: bool = False,
    ) -> None:
        super().__init__(image, pos, type, size)
        self.is_special = special
        self.vel = 0.3

    def update(self, dt: float):
        dy = self.vel * dt * godspeed.common.universal_speedup
        if self.is_special:
            self.pos.y += dy
            if self.pos.y >= SCREEN_SIZE[1]:
                self.pos.y = -SCREEN_SIZE[1] + dy
            self.rect.topleft = self.pos
            return

        super().update()
        self.pos.y += dy * 0.9
        self.rect.topleft = self.pos

    def draw(self, screen):
        if self.is_special:
            if self.rect.x < SCREEN_SIZE[0] / 2:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x - 94 + 29, self.rect.y))
        else:
            screen.blit(self.image, self.rect)


@dataclass
class _ScaleOffset:
    """
    A class that provides information on how much to 
    scale either the left or right platform

    Details:
    This is because the platform image has 
    leaves that shouldn't be considered
    when calculating its hitbox
    """

    scale_x: int
    scale_y: int

@dataclass
class _PixelBufferOffset:
    """
    A class that gives information about
    how many pixels to offset from (0, 0) for the 
    left or right platforms when drawing
    """
    x_pad: int
    y_pad: int

@dataclass 
class _PixelOffsets:
    """
    A class that contains information on how much to offset 
    platforms while scaling and drawing
    """
    pixel_buffer_offset: _PixelBufferOffset
    scale_offset: _ScaleOffset


class _SpecialPlatformSides(enum.Enum):
    LEFT = _PixelOffsets(
        _PixelBufferOffset(0, 0),
        _ScaleOffset(scale_x=93, scale_y=SCREEN_SIZE[1])
    )
    RIGHT = _PixelOffsets(
        _PixelBufferOffset(SCREEN_SIZE[0] - PLAT_WIDTH, 0),
        _ScaleOffset(scale_x=93, scale_y=SCREEN_SIZE[1])
    )


def _rectify_side_platform_image(image: pygame.Surface, side: _SpecialPlatformSides) -> pygame.Surface:
    """
    Rectifies specific image
    """
    image = pygame.transform.scale(
        image,
        (side.value.scale_offset.scale_x, side.value.scale_offset.scale_y)
    )


def rectify_side_platform_images() -> None:
    """
    Rectifies the side platform image
    """
    bamboo_image_number = 1
    assets_ref = godspeed.common.assets
    for side in _SpecialPlatformSides:
        path = f"bamboo_{bamboo_image_number}"
        image = assets_ref[path]
        assets_ref[path] = _rectify_side_platform_image(image, side)
        bamboo_image_number *= -1
    


def create_side_platforms() -> list[Platform]:
    """
    Creates the side platforms.
    """
    platforms = []
    bamboo_image_number = 1
    for side in _SpecialPlatformSides:
        path = f"bamboo_{bamboo_image_number}"
        platform = Platform(
            image=godspeed.common.assets[path],
            pos=(side.value.pixel_buffer_offset.x_pad, side.value.pixel_buffer_offset.y_pad),
            type=Entities.PLATFORM,
            size=(PLAT_WIDTH, SCREEN_SIZE[1])
        )
        platforms.append(platform)
        bamboo_image_number *= -1
    
    return platforms
