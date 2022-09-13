import pygame

from game.load import load_images
from library.utils.classes import Time
from game.common import SCREEN_SIZE


class LoadingScreen:
    """A loading screen."""
    FONT = pygame.font.SysFont("consolas", 40)

    def __init__(self, state: str) -> None:
        self.state = state
        self.assets = {
            "loading_screen": pygame.transform.scale(
                    pygame.image.load("assets/images/backgrounds/loading_screen.png").convert_alpha(),
                    SCREEN_SIZE
                )
        }
        self.loading = True
        self.loading_text = "Loading"
        self.loading_t = Time(0.7)
        self.t = Time(10)
    
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
        if list(asset)[0] in self.assets and self.t.update():
            self.loading = False 
            return 

        self.assets |= asset


    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.assets["loading_screen"], (0, 0))
        loading_text_surf = self.FONT.render(self.loading_text, True, "black")
        screen.blit(loading_text_surf, (100, 500))
        pygame.display.flip()


