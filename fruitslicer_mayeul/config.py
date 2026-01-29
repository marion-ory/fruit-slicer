import os
import pygame

# === DIMENSIONS ===
LOGICAL_WIDTH, LOGICAL_HEIGHT = 800, 600
FPS = 60

# === COULEURS ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (240, 220, 70)
ORANGE = (255, 165, 0)

# === CHEMINS ===
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# === PARAMÈTRES JEU ===
FREEZE_DURATION_MS = 4000

DIFFICULTY_SETTINGS = {
    "EASY": {
        "fruit_per_beat": 1,
        "bomb_chance": 0.08,
        "speed_multiplier": 0.8,
    },
    "HARD": {
        "fruit_per_beat": 2,
        "bomb_chance": 0.18,
        "speed_multiplier": 1.2,
    },
}

# === INITIALISATION PYGAME ===
pygame.init()
pygame.mixer.init()

WINDOW = pygame.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Fruit Slicer")

SCREEN = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))
CLOCK = pygame.time.Clock()

# === CHARGEMENT IMAGES ===
def load_image(name, scale=None):
    path = os.path.join(ASSETS_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.smoothscale(img, scale)
    return img

# Backgrounds
BACKGROUND_MENU = load_image("backgroundmenu.jpg", (LOGICAL_WIDTH, LOGICAL_HEIGHT))
BACKGROUND_GAME = load_image("backgroundjeu.jpg", (LOGICAL_WIDTH, LOGICAL_HEIGHT))

# Logo
LOGO = load_image("logo.png", (416, 156))

# Fruits
IMG_APPLE = load_image("apple.png", (64, 64))
IMG_APPLE_SLICE = load_image("appleslice.png", (58, 58))
IMG_BANANA = load_image("banana.png", (80, 64))
IMG_BANANA_SLICE = load_image("bananaslice.png", (72, 58))
IMG_ORANGE = load_image("orange.png", (64, 64))
IMG_ORANGE_SLICE = load_image("orangeslice.png", (58, 58))

# Spéciaux
IMG_ICE = load_image("icecube.png", (64, 64))
IMG_BOMB = load_image("bomb.png", (74, 74))
IMG_GOLDENFRUIT = load_image("goldenfruit.png", (64, 64))
IMG_GOLDENFRUIT_SLICE = load_image("goldenfruitslice.png", (58, 58))

# UI
IMG_COMBO = load_image("combo.png", (200, 80))
IMG_HEART = load_image("heart.png", (32, 32))

# Fonts
FONT_BIG = pygame.font.Font(None, 64)
FONT_MED = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)
