import pygame

from game.common import SCREEN_SIZE
from game.entities.enums import Entities
from game.entities.platform import Platform
from game.entities.player import Player


class WorldInitStage:
    def __init__(self) -> None:
        self.player = Player()
        self.platforms: list[Platform] = []
        self.alive = True


class PlayerStage(WorldInitStage):
    def update(self, event_info):
        self.player.update(event_info)

    def draw(self, screen):
        self.player.draw(screen)


class PlatformStage(PlayerStage):
    def __init__(self) -> None:
        super().__init__()
        plat_size = self.player.SIZE[0]
        rows = 0, int((SCREEN_SIZE[0] - plat_size) / plat_size)
        n_cols = int(SCREEN_SIZE[1] / plat_size)
        for row in rows:
            for col in range(n_cols):
                plat_image = pygame.Surface(self.player.SIZE)
                plat_pos = pygame.Vector2(row * plat_size, col * plat_size)
                print(plat_pos)
                self.platforms.append(Platform(plat_image, plat_pos, Entities.PLATFORM))

    def update(self, event_info):
        for plat in self.platforms[:]:
            plat.update(event_info)

            if not plat.alive:
                self.platforms.remove(plat)
                print("PLATFORM REMOVED: ", plat)

    def draw(self, screen):
        for plat in self.platforms:
            plat.draw(screen)


class World(PlatformStage):
    pass
