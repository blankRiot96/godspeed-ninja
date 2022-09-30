import pygame
import pathlib

SCREEN_SIZE = 400, 670
SCREEN_RECT = pygame.Rect(0, 0, *SCREEN_SIZE)
SCORE = 0
UNIVERSAL_SPEEDUP = 1
assets = {}

# PATHS
IMAGE_PATH = pathlib.Path("assets/images/")
FONT_PATH = pathlib.Path("assets/fonts/")
