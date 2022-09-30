import pygame
from pglib.sprite.surf import FadingImage
from pglib.utils import font
from pglib.ui.buttons import Button

import godspeed.common
from godspeed.common import SCREEN_SIZE, FONT_PATH, SCREEN_RECT
from godspeed.states.abc import GameState
from godspeed.states.enums import States


def create_fading_overlay() -> FadingImage:
    surf = pygame.Surface(SCREEN_SIZE)
    return FadingImage(
        image=surf,
        speed=3,
        duration=1,
        pos=(0, 0),
    )

def create_retry_button() -> Button:
    font_name = FONT_PATH / "IBM_Plex_Sans" / "IBMPlexSans-Bold.ttf"
    rect = pygame.Rect((0, 0), (170, 50))
    rect.center = SCREEN_RECT.center
    return Button(
        pos=rect.topleft,
        size=rect.size,
        colors={
            "static": "grey",
            "hover": "red",
            "text": "white"
        },
        font_name=font_name,
        text="RETRY",
        corner_radius=3,
    )

class DeathInitStage:
    def __init__(self) -> None:
        super().__init__()
        self.transition_overlay = create_fading_overlay()

    def update(self, event_info):
        pass 

    def draw(self, screen):
        pass

class RenderBackgroundStage(DeathInitStage):
    def update(self, event_info): 
        super().update(event_info)
        if self.transition_overlay.alpha < 155:
            self.transition_overlay.update(event_info["dt"])

    def draw_last_frame_of_gameplay(self, screen):
        gameplay_last_frame = self.receive_data[States.WORLD]["last_screen"]
        screen.blit(gameplay_last_frame, (0, 0))

    def draw(self, screen): 
        super().draw(screen)
        self.draw_last_frame_of_gameplay(screen)
        self.transition_overlay.draw(screen)

class RenderInfo(RenderBackgroundStage):
    SCORE_FONT = font(
        size=40, name=FONT_PATH / "IBM_Plex_Sans" / "IBMPlexSans-Bold.ttf"
    )
    

    def __init__(self) -> None:
        super().__init__()
        self.anim_score = 0
        self.retry_button = create_retry_button()

    def update(self, event_info):
        super().update(event_info)
        self.anim_score += 1.3 * event_info["dt"]
        if self.anim_score > godspeed.common.SCORE:
            self.anim_score = godspeed.common.SCORE

        self.retry_button.update(event_info["mouse_pos"], event_info["mouse_press"])
        if self.retry_button.clicked:
            self.end()

    def end(self) -> None:
        self.alive = False
        self.next_state = States.WORLD

    def draw_score(self, screen):
        score_surf = self.SCORE_FONT.render(
            f"SCORE: {self.anim_score:.0f}", True, "white"
        )
        score_surf_rect = score_surf.get_rect()
        score_surf_rect.midtop = SCREEN_RECT.midtop
        screen.blit(score_surf, score_surf_rect)
    
    def draw_retry_button(self, screen):
        self.retry_button.draw(screen)

    def draw(self, screen):
        super().draw(screen)
        self.draw_score(screen)
        self.draw_retry_button(screen)


class DeathScreen(GameState, RenderInfo):
    """Death screen to appear after player dies."""
    def __init__(self) -> None:
        super().__init__()
