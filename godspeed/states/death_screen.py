import pygame
from pglib.sprite.surf import FadingImage
from pglib.ui.buttons import Button
from pglib.utils import font

import godspeed.common
from godspeed.common import IBM_FONTS_PATHS, SCREEN_RECT, SCREEN_SIZE
from godspeed.states.abc import GameState
from godspeed.states.enums import States


def create_fading_overlay() -> FadingImage:
    return FadingImage(
        image=pygame.Surface(SCREEN_SIZE),
        speed=3,
        duration=1,
        pos=(0, 0),
    )


def create_retry_button() -> Button:
    font_name = IBM_FONTS_PATHS["bold"]
    rect = pygame.Rect((0, 0), (170, 50))
    rect.center = SCREEN_RECT.center
    return Button(
        pos=rect.topleft,
        size=rect.size,
        colors={"static": "grey", "hover": "red", "text": "white"},
        font_name=font_name,
        text="RETRY",
        corner_radius=3,
    )


class DeathInitStage:
    def __init__(self) -> None:
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
    SCORE_FONT = font(size=40, name=IBM_FONTS_PATHS["bold"])
    SCORE_FACTOR = 1.3

    def __init__(self) -> None:
        super().__init__()
        self.anim_score = 0
        self.retry_button = create_retry_button()

    def update(self, event_info):
        super().update(event_info)
        self.anim_score += self.SCORE_FACTOR * event_info["dt"]
        if self.anim_score > godspeed.common.score:
            self.anim_score = godspeed.common.score

        self.retry_button.update(event_info["mouse_pos"], event_info["mouse_press"])
        if self.retry_button.clicked:
            self.end()

    def end(self) -> None:
        self.active = False
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
