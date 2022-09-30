import pathlib

import pygame

SCREEN_SIZE = 400, 670
SCREEN_RECT = pygame.Rect(0, 0, *SCREEN_SIZE)
score = 0
universal_speedup = 1
assets = {}

# PATHS
IMAGE_PATH = pathlib.Path("assets/images/")
FONT_PATH = pathlib.Path("assets/fonts/")

# IBM
IBM_FONT_PATH = FONT_PATH / "IBM_Plex_Sans"
IBM_TTF_FORMAT = "IBM_Plex_Sans/" + "IBMPlexSans-{}"
IBM_FONTS_PATHS = {
    "light": IBM_TTF_FORMAT.format("Light"),
    "extra_light": IBM_TTF_FORMAT.format("ExtraLight"),
    "bold": IBM_TTF_FORMAT.format("Bold"),
}
