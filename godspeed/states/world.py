import colorsys
import random

import pygame
from pglib.common import EventInfo
from pglib.ui.loading_bar import LoadingBar
from pglib.ui.loading_screen import LoadingScreen
from pglib.utils.classes import Time

import godspeed.common
from godspeed.common import FONT_PATH, IMAGE_PATH, SCREEN_SIZE
from godspeed.entities.enums import Entities
from godspeed.entities.obstacles import Shuriken, Spike
from godspeed.entities.platform import Platform
from godspeed.entities.player import Player


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


class LoadingScreenStage(WorldInitStage):
    def __init__(self) -> None:
        super().__init__()
        loading_screen = pygame.image.load(
            IMAGE_PATH / "backgrounds" / "loading_screen.png"
        ).convert()
        loading_screen = pygame.transform.scale(loading_screen, SCREEN_SIZE)
        godspeed.common.assets |= {"loading_screen": loading_screen}
        self.loading_screen = LoadingScreen(
            "world",
            godspeed.common.assets,
            LoadingBar(
                "grey",
                "white",
                pygame.Rect((0, SCREEN_SIZE[1] - 20), (SCREEN_SIZE[0], 20)),
            ),
            font=pygame.font.Font(
                FONT_PATH / "IBM_Plex_Sans" / "IBMPlexSans-Light.ttf", 20
            ),
            font_color="white",
            debug_timer=0.1,
        )

        while self.loading_screen.loading:
            self.loading_screen.update()
            self.loading_screen.draw(pygame.display.get_surface())


class BackgroundRenderStage(LoadingScreenStage):
    def __init__(self) -> None:
        super().__init__()
        bg = godspeed.common.assets["bg"]
        godspeed.common.assets["bg"] = pygame.transform.scale(bg, SCREEN_SIZE)
        self.uncolored_bg = godspeed.common.assets["bg"].copy()

    def update(self, event_info: EventInfo):
        super().update(event_info)
        bg_copy = self.uncolored_bg.copy()
        tint = ((self.player.distance_covered / 50) % 100) / 100
        color = colorsys.hsv_to_rgb(tint, 1, 0.5)
        bg_copy.fill(
            (color[0] * 255, color[1] * 255, color[2] * 255),
            special_flags=pygame.BLEND_ADD,
        )
        godspeed.common.assets["bg"] = bg_copy.copy()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        screen.blit(godspeed.common.assets["bg"], (0, 0))


class PlatformStage(BackgroundRenderStage):
    PLATFORM_INTRO_SCORE = 1000

    def __init__(self) -> None:
        super().__init__()
        platform_image_name = "bamboo_{n}"
        print(godspeed.common.assets)
        n = 1
        for i in range(2):
            for row in 0, SCREEN_SIZE[0] - self.player.SIZE[0]:
                image: pygame.Surface = godspeed.common.assets[
                    platform_image_name.format(n=n)
                ]
                image = image.subsurface(image.get_bounding_rect())
                size = (29, SCREEN_SIZE[1])
                image = pygame.transform.scale(image, (size[0] + 64, size[1]))
                if row != 0:
                    image = pygame.transform.flip(image, True, False)

                self.platforms.append(
                    Platform(
                        image,
                        pygame.Vector2(
                            row if row == 0 else row + 20, 0 - (i * SCREEN_SIZE[1])
                        ),
                        Entities.PLATFORM,
                        size=size,
                        special=True,
                    )
                )
                n *= -1
        self.plat_gen_time = Time(5)

    def update(self, event_info):
        super().update(event_info)

        for plat in self.platforms[:]:
            plat.update(event_info["dt"])

            if not plat.alive:
                self.platforms.remove(plat)

        # Everything after this if statement
        # is only for when the player reaches a
        # certain score.
        if godspeed.common.SCORE < self.PLATFORM_INTRO_SCORE:
            return

        if self.plat_gen_time.update():
            width = 30
            height = random.randrange(2, 5) * width
            size = (width, height)
            image = pygame.Surface(size)
            pos_x = random.choice(tuple(x * width for x in range(2, 5)))
            plat = Platform(image, pygame.Vector2(pos_x, -height), Entities.PLATFORM)

            self.platforms.append(plat)

    def draw(self, screen):
        super().draw(screen)
        for plat in self.platforms:
            plat.draw(screen)


class ShurikenStage(PlatformStage):
    SHURIKEN_INTRO_SCORE = 500

    def __init__(self) -> None:
        super().__init__()
        self.shuriken_gen_time = Time(3.0)

    def update(self, event_info: EventInfo):
        super().update(event_info)

        if godspeed.common.SCORE < self.SHURIKEN_INTRO_SCORE:
            return

        if self.shuriken_gen_time.update():
            pos_x = random.randrange(50, SCREEN_SIZE[0] - 50)
            self.shurikens.append(Shuriken(pygame.Vector2(pos_x, -50)))

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
        if godspeed.common.SCORE < self.SPIKE_INTRO_SCORE:
            return

        if self.spike_gen_time.update():
            spike_height = 30
            dir = random.choice(("left", "right"))

            if dir == "left":
                pos_x = 29
            else:
                pos_x = SCREEN_SIZE[0] - (spike_height + 29)

            n_spikes = random.randrange(2, 5)

            for x in range(n_spikes):
                self.spikes.append(
                    Spike(
                        spike_height,
                        pygame.Vector2(
                            pos_x, (x * spike_height) - (n_spikes * spike_height)
                        ),
                        dir,
                    )
                )

        for spike in self.spikes[:]:
            spike.update(event_info["dt"])

            if not spike.alive:
                self.spikes.remove(spike)

    def draw(self, screen):
        super().draw(screen)
        for spike in self.spikes:
            spike.draw(screen)


class ScoreStage(SpikeStage):
    SCORE_FONT = pygame.font.SysFont("comicsans", 40)

    def __init__(self) -> None:
        super().__init__()
        self.score_vel = 0.1
        self.score_acc = 0.001

    def update(self, event_info):
        super().update(event_info)
        if godspeed.common.SCORE < 150 or godspeed.common.SCORE % 100 == 0:
            self.score_vel += self.score_acc * event_info["dt"]
        godspeed.common.SCORE += self.score_vel * event_info["dt"]
        godspeed.common.UNIVERSAL_SPEEDUP = self.score_vel * 20 if self.score_vel else godspeed.common.UNIVERSAL_SPEEDUP

    def draw(self, screen):
        super().draw(screen)
        score_surf = self.SCORE_FONT.render(f"{godspeed.common.SCORE:.0f}", True, "black")
        score_rect = score_surf.get_rect()
        score_rect.center = screen.get_rect().center
        screen.blit(score_surf, score_rect)


class PlayerStage(ScoreStage):
    def handle_player_platform_collision(self, dt: float):
        for plat in self.platforms:
            if (
                self.player.would_collide(plat, dt)
                and not self.player.is_space_pressed
            ):
                self.player.vel = 0
                if self.player.rect.x > plat.rect.x:
                    self.player.pos.x = plat.rect.left + plat.size[0]
                else:
                    self.player.pos.x = (
                        plat.rect.right - self.player.SIZE[0] - plat.size[0]
                    )

                break

    def handle_player_spike_collision(self):
        for spike in self.spikes:
            if self.player.collides(spike):
                self.player.alive = False 
                break

    def update(self, event_info):
        super().update(event_info)
        if self.player.alive:
            self.player.handle_input(event_info["events"])

        # Handle Player collision with other entities
        self.player.vel = self.player.VEL
        self.handle_player_platform_collision(event_info["dt"])
        self.handle_player_spike_collision()

        if not self.player.alive:
            godspeed.common.UNIVERSAL_SPEEDUP = -(abs(godspeed.common.UNIVERSAL_SPEEDUP))
            self.score_acc = 0
            self.score_vel = 0
        
        if self.player.pos.x > SCREEN_SIZE[0] or self.player.pos.x + self.player.SIZE[0] < 0:
            godspeed.common.UNIVERSAL_SPEEDUP = 0
            self.player.alive = True

        self.player.update(event_info["dt"])



    def draw(self, screen):
        super().draw(screen)
        self.player.draw(screen)


class World(PlayerStage):
    pass
