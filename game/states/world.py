import pygame
import random

import game.common
from game.common import SCREEN_SIZE
from game.entities.enums import Entities
from game.entities.platform import Platform
from game.entities.obstacles import Spike
from game.entities.player import Player

from library.common import EventInfo
from library.utils.classes import Time


class WorldInitStage:
    def __init__(self) -> None:
        self.player = Player()
        self.platforms: list[Platform] = []
        self.spikes: list[Spike] = []
        self.alive = True

    def update(self, event_info: EventInfo):
        pass 

    def draw(self, screen: pygame.Surface):
        pass

class SpikeStage(WorldInitStage):
    def __init__(self) -> None:
        super().__init__()
        self.spike_gen_time = Time(2.5)

    def update(self, event_info):
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
                    Spike(spike_height, pygame.Vector2(pos_x, x * spike_height), dir)
                )

        for spike in self.spikes:
            spike.update(event_info["dt"])
    
    def draw(self, screen):
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
                if self.player.pos.x < 100:
                    self.player.pos.x = 49
                else:
                    self.player.pos.x = SCREEN_SIZE[0] - 99

        self.player.update(event_info["dt"])

    def draw(self, screen):
        super().draw(screen)
        self.player.draw(screen)


class ScoreStage(PlayerStage):
    SCORE_FONT = pygame.font.SysFont("comicsans", 40)

    def __init__(self) -> None:
        super().__init__()
        self.score_gen_time = Time(1)
    
    def update(self, event_info):
        super().update(event_info)
        if self.score_gen_time.update():
            game.common.SCORE += 1
            self.score_gen_time.time_to_pass += 3.3
        
        game.common.UNIVERSAL_SPEEDUP = (game.common.SCORE + 1) * 0.7

    def draw(self, screen):
        super().draw(screen)
        score_surf = self.SCORE_FONT.render(str(game.common.SCORE), True, "black")
        score_rect = score_surf.get_rect()
        score_rect.center = screen.get_rect().center
        screen.blit(score_surf, score_rect)

class PlatformStage(ScoreStage):
    def __init__(self) -> None:
        super().__init__()
        for row in 0, SCREEN_SIZE[0] - self.player.SIZE[0]:
            self.platforms.append(Platform(
                pygame.Surface((self.player.SIZE[0], SCREEN_SIZE[1])),
                pygame.Vector2(row, 0),
                Entities.PLATFORM
            ))
        

    def update(self, event_info):
        super().update(event_info)
        
        
    def draw(self, screen):
        super().draw(screen)
        for plat in self.platforms:
            plat.draw(screen)


class World(PlatformStage):
    pass
