import asyncio
import itertools

import pygame

from src.common import SCREEN_SIZE
from src.states.main_menu import MainMenu
from src.states.world import World


class Game:
    SCREEN_FLAGS = pygame.SCALED
    FPS_CAP = 60

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(SCREEN_SIZE, self.SCREEN_FLAGS)
        self.clock = pygame.time.Clock()
        self.states = itertools.cycle((World, MainMenu))
        self.state = World()

        self._is_running = True

    def _grab_events(self):
        """
        Return window events
        """
        raw_dt = self.clock.get_time() / 1000
        # capping delta time to avoid bugs when moving the window
        dt = min(raw_dt * 100, 10)
        events = pygame.event.get()
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        key_press = pygame.key.get_pressed()

        return {
            "raw_dt": raw_dt,
            "dt": dt,
            "events": events,
            "mouse_press": mouse_press,
            "mouse_pos": mouse_pos,
            "key_press": key_press,
        }

    def _update(self) -> None:
        event_info = self._grab_events()
        for event in event_info["events"]:
            if event.type == pygame.QUIT:
                self._is_running = False

        self.state.update(event_info)
        if not self.state.alive:
            self.state = next(self.states)()

    def _draw(self) -> None:
        self.screen.fill("grey")
        self.state.draw(self.screen)

    async def _run(self) -> None:
        while self._is_running:
            self._update()
            self._draw()

            pygame.display.set_caption(
                f"Godspeed Ninja | {self.clock.get_fps():.0f} FPS"
            )

            self.clock.tick(self.FPS_CAP)
            pygame.display.flip()
            await asyncio.sleep(0)

    def run(self) -> None:
        asyncio.run(self._run())
