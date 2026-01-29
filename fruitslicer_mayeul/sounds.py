import os
import pygame
from config import BASE_DIR

# === CHEMINS ===
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
MUSIC_FILE = os.path.join(MUSIC_DIR, "track.mp3")

# === EFFETS SONORES ===
SFX_FRUIT = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "fruit.mp3"))
SFX_GOLDENFRUIT = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "goldenfruit.mp3"))
SFX_BOMB = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "bomb.mp3"))
SFX_COMBO = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "combo.mp3"))

# Volumes
SFX_FRUIT.set_volume(0.7)
SFX_GOLDENFRUIT.set_volume(0.8)
SFX_BOMB.set_volume(0.9)
SFX_COMBO.set_volume(0.9)

# === FONCTIONS ===
def play_fruit_sound():
    SFX_FRUIT.play()

def play_golden_sound():
    SFX_GOLDENFRUIT.play()

def play_bomb_sound():
    SFX_BOMB.play()

def play_combo_sound():
    SFX_COMBO.play()

def start_music():
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()
