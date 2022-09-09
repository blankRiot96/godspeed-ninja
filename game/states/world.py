import pygame

import game.common
from game.common import SCREEN_SIZE
from game.entities.enums import Entities
from game.entities.platform import Platform
from game.entities.player import Player


class WorldInitStage:
    def __init__(self) -> None:
        self.player = Player()
        self.left_platforms: list[Platform] = []
        self.right_platforms: list[Platform] = []
        self.alive = True


class PlayerStage(WorldInitStage):
    def update(self, event_info):
        self.player.update(event_info)

    def draw(self, screen):
        self.player.draw(screen)


class ScoreStage(PlayerStage):
    MIN_TILES_PASSED = 5
    SCORE_FONT = pygame.font.SysFont("comicsans", 40)

    def __init__(self) -> None:
        super().__init__()
        self.tiles_passed = 0
    
    def draw(self, screen):
        super().draw(screen)
        score_surf = self.SCORE_FONT.render(str(game.common.SCORE), True, "black")
        score_rect = score_surf.get_rect()
        score_rect.center = screen.get_rect().center
        screen.blit(score_surf, score_rect)

class PlatformStage(ScoreStage):
    def __init__(self) -> None:
        super().__init__()
        plat_size = self.player.SIZE[0]
        self.rows = 0, int((SCREEN_SIZE[0] - plat_size) / plat_size)
        n_cols = int(SCREEN_SIZE[1] / plat_size)
        for col in range(-plat_size, n_cols, 1):
            plat_image = pygame.Surface(self.player.SIZE)
            plat_pos = pygame.Vector2(self.rows[0] * plat_size, col * plat_size)
            self.left_platforms.append(Platform(plat_image, plat_pos, Entities.PLATFORM))

        for col in range(-plat_size, n_cols, 1):
            plat_image = pygame.Surface(self.player.SIZE)
            plat_pos = pygame.Vector2(self.rows[1] * plat_size, col * plat_size)
            self.right_platforms.append(Platform(plat_image, plat_pos, Entities.PLATFORM))

    def update(self, event_info):
        super().update(event_info)
        for platforms in (self.left_platforms, self.right_platforms):
            head = platforms[-1]
            head.update(event_info)
            for plat, next_plat in zip(platforms[:-1], platforms[1:]):
                plat.rect.bottomleft = next_plat.rect.topleft

            if not head.alive:
                platforms.pop()
                new_plat = Platform(
                    pygame.Surface(self.player.SIZE),
                    platforms[0].pos + self.player.SIZE,
                    Entities.PLATFORM
                )
                platforms.insert(0, new_plat)
                self.tiles_passed += 1
                if self.tiles_passed == self.MIN_TILES_PASSED:
                    game.common.SCORE += 1
                    self.tiles_passed = 0

    def draw(self, screen):
        super().draw(screen)
        for plat in self.left_platforms:
            plat.draw(screen)

        for plat in self.right_platforms:
            plat.draw(screen)


class World(PlatformStage):
    pass
