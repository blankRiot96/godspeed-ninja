import pygame
from library.utils.classes import Time

import game.common
from game.common import SCREEN_SIZE
from game.load import load_images


class LoadingScreen:
    """A loading screen."""

    FONT = pygame.font.SysFont("comicsansms", 40)

    def __init__(self, state: str) -> None:
        self.state = state
        self.loading = True
        self.loading_text = "Loading"
        self.loading_t = Time(0.7)
        game.common.assets = {
            "loading_screen": pygame.transform.scale(
                pygame.image.load(
                    "assets/images/backgrounds/loading_screen.png"
                ).convert_alpha(),
                SCREEN_SIZE,
            )
        }
        self.t = Time(3)

    def loading_text_mod(self):
        if self.loading_t.update():
            self.loading_text += "."
            if self.loading_text == "Loading....":
                self.loading_text = "Loading"

    def update(self) -> None:
        pygame.event.get()
        self.loading_text_mod()

        asset = next(load_images(self.state))

        # Checking if the asset is the same, i.e, done loading
        if list(asset)[0] in game.common.assets and self.t.update():
            self.loading = False
            return

        game.common.assets |= asset

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(game.common.assets["loading_screen"], (0, 0))
        loading_text_surf = self.FONT.render(self.loading_text, True, "black")
        screen.blit(loading_text_surf, (120, 550))
        pygame.display.flip()
