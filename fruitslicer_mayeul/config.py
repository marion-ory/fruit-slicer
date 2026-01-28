# config.py

import os
import pygame

LOGICAL_WIDTH, LOGICAL_HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (240, 220, 70)
ORANGE = (255, 165, 0)

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MUSIC_DIR = os.path.join(BASE_DIR, "music")

MUSIC_FILE = os.path.join(MUSIC_DIR, "track.mp3")

FONT_NAME = None

DIFFICULTY_SETTINGS = {
    "EASY": {
        "fruit_per_beat": 1,
        "bomb_chance": 0.03,
        "speed_multiplier": 0.8,
    },
    "HARD": {
        "fruit_per_beat": 2,
        "bomb_chance": 0.10,
        "speed_multiplier": 1.2,
    },
}

FREEZE_DURATION_MS = 4000  # Durée du slow-motion
COMBO_WINDOW_MS = 500  # Fenêtre pour faire un combo

# Système de combo
COMBO_MULTIPLIERS = {
    0: 1,   # x1
    3: 2,   # x2 à partir de 3 hits
    5: 3,   # x3 à partir de 5 hits
    8: 4,   # x4 à partir de 8 hits
}

COMBO_FOR_LIFE = 15  # Nombre de combos pour gagner une vie

pygame.init()
pygame.mixer.init()

WINDOW = pygame.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Fruit Slicer")

SCREEN = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))
CLOCK = pygame.time.Clock()

def load_image(name, scale=None):
    path = os.path.join(ASSETS_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    if scale is not None:
        img = pygame.transform.smoothscale(img, scale)
    return img

BACKGROUND_MENU = load_image("backgroundmenu.jpg", (LOGICAL_WIDTH, LOGICAL_HEIGHT))
BACKGROUND_GAME = load_image("backgroundjeu.jpg", (LOGICAL_WIDTH, LOGICAL_HEIGHT))

LOGO = load_image("logo.png", (416, 156))

IMG_APPLE = load_image("apple.png", (64, 64))
IMG_APPLE_SLICE = load_image("appleslice.png", (64, 64))
IMG_BANANA = load_image("banana.png", (80, 64))
IMG_BANANA_SLICE = load_image("bananaslice.png", (80, 64))
IMG_ORANGE = load_image("orange.png", (64, 64))
IMG_ORANGE_SLICE = load_image("orangeslice.png", (64, 64))

IMG_ICE = load_image("icecube.png", (64, 64))
IMG_BOMB = load_image("bomb.png", (64, 64))
IMG_GOLDENFRUIT = load_image("goldenfruit.png", (64, 64))

IMG_COMBO = load_image("combo.png", (200, 80))
IMG_HEART = load_image("heart.png", (32, 32))
IMG_SPLASH = load_image("splash.png", (64, 64))
IMG_SLICE = load_image("slice.png", (100, 20))

FONT_BIG = pygame.font.Font(FONT_NAME, 64)
FONT_MED = pygame.font.Font(FONT_NAME, 36)
FONT_SMALL = pygame.font.Font(FONT_NAME, 24)
