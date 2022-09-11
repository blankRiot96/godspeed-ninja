import pygame
import random

import game.common
from game.common import SCREEN_SIZE
from game.entities.enums import Entities
from game.entities.platform import Platform
from game.entities.obstacles import Spike, Shuriken
from game.entities.player import Player

from library.common import EventInfo
from library.utils.classes import Time


class WorldInitStage:
    def __init__(self) -> None:
        self.player = Player()
        self.platforms: list[Platform] = []
        self.spikes: list[Spike] = []
        self.shurikens: list[Shuriken] = []
        self.alive = True

    def update(self, event_info: EventInfo):
        pass 

    def draw(self, screen: pygame.Surface):
        pass


class ShurikenStage(WorldInitStage):
    SHURIKEN_INTRO_SCORE = 500

    def __init__(self) -> None:
        super().__init__()
        self.shuriken_gen_time = Time(3.0)

    def update(self, event_info: EventInfo):
        super().update(event_info)

        if game.common.SCORE < self.SHURIKEN_INTRO_SCORE:
            return 

        if self.shuriken_gen_time.update():
            pos_x = random.randrange(50, SCREEN_SIZE[0] - 50)
            self.shurikens.append(
                Shuriken(
                    pygame.Vector2(pos_x, -50)
                )
            )

        for shuriken in self.shurikens[:]:
            shuriken.update(event_info["dt"])
            if not shuriken.alive:
                self.shurikens.remove(shuriken)

    def draw(self, screen):
        super().draw(screen)
        for shuriken in self.shurikens:
            shuriken.draw(screen)

class SpikeStage(ShurikenStage):
    SPIKE_INTRO_SCORE = 100

    def __init__(self) -> None:
        super().__init__()
        self.spike_gen_time = Time(2.5)

    def update(self, event_info):
        super().update(event_info)
        if game.common.SCORE < self.SPIKE_INTRO_SCORE:
            return

        if self.spike_gen_time.update():
            spike_height = 30
            dir = random.choice(("left", "right"))

            if dir == "left":
                pos_x = 50
            else:
                pos_x = SCREEN_SIZE[0] - 80

            n_spikes = random.randrange(2, 5)

            for x in range(n_spikes):
                self.spikes.append(
                    Spike(spike_height, pygame.Vector2(pos_x, (x * spike_height) - (n_spikes * spike_height)), dir)
                )

        for spike in self.spikes[:]:
            spike.update(event_info["dt"])

            if not spike.alive:
                self.spikes.remove(spike)
    
    def draw(self, screen):
        super().draw(screen)
        for spike in self.spikes:
            spike.draw(screen)


class PlayerStage(SpikeStage):
    def update(self, event_info):
        super().update(event_info)
        self.player.handle_input(event_info["events"])
        
        # Handle Player-Platform collision 
        self.player.vel = self.player.VEL
        for plat in self.platforms:
            if self.player.collides(plat) and not self.player.is_space_pressed:
                self.player.vel = 0

                if self.player.pos.x - plat.pos.x > 0:
                    self.player.rect.left = plat.rect.right 
                elif self.player.pos.x - plat.pos.x < 0:
                    self.player.rect.right = plat.rect.left 

                break

        self.player.update(event_info["dt"])

    def draw(self, screen):
        super().draw(screen)
        self.player.draw(screen)


class ScoreStage(PlayerStage):
    SCORE_FONT = pygame.font.SysFont("comicsans", 40)

    def __init__(self) -> None:
        super().__init__()
        self.score_vel = 0.1
        self.score_acc = 0.001

    def update(self, event_info):
        super().update(event_info)
        if game.common.SCORE < 150 or game.common.SCORE % 100 == 0:
            self.score_vel += self.score_acc * event_info["dt"]
        game.common.SCORE += self.score_vel * event_info["dt"]        
        game.common.UNIVERSAL_SPEEDUP = self.score_vel * 20

    def draw(self, screen):
        super().draw(screen)
        score_surf = self.SCORE_FONT.render(f"{game.common.SCORE:.0f}", True, "black")
        score_rect = score_surf.get_rect()
        score_rect.center = screen.get_rect().center
        screen.blit(score_surf, score_rect)

class PlatformStage(ScoreStage):
    PLATFORM_INTRO_SCORE = 1000

    def __init__(self) -> None:
        super().__init__()
        for row in 0, SCREEN_SIZE[0] - self.player.SIZE[0]:
            self.platforms.append(Platform(
                pygame.Surface((self.player.SIZE[0], SCREEN_SIZE[1])),
                pygame.Vector2(row, 0),
                Entities.PLATFORM,
                special=True
            ))
        self.plat_gen_time = Time(5)
        

    def update(self, event_info):
        super().update(event_info)
        
        if game.common.SCORE < self.PLATFORM_INTRO_SCORE:
            return 
        
        if self.plat_gen_time.update():
            width = 30
            height = random.randrange(2, 5) * width
            size = (width, height)
            image = pygame.Surface(size)
            pos_x = random.choice(tuple(x * width for x in range(2, 5)))
            plat = Platform(image, pygame.Vector2(pos_x, -height), Entities.PLATFORM)

            self.platforms.append(plat)

        for plat in self.platforms[:]:
            if not plat.is_special:
                plat.update(event_info["dt"])

            if not plat.alive:
                self.platforms.remove(plat)

        
    def draw(self, screen):
        super().draw(screen)
        for plat in self.platforms:
            plat.draw(screen)


class World(PlatformStage):
    pass
