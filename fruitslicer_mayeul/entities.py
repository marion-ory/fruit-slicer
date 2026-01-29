import random
import pygame
from config import *

# === TYPES D'OBJETS ===
FRUIT_TYPES = [
    {"name": "APPLE", "img": IMG_APPLE, "img_slice": IMG_APPLE_SLICE, "base_points": 1},
    {"name": "BANANA", "img": IMG_BANANA, "img_slice": IMG_BANANA_SLICE, "base_points": 1},
    {"name": "ORANGE", "img": IMG_ORANGE, "img_slice": IMG_ORANGE_SLICE, "base_points": 1},
]

ICE_TYPE = {"name": "ICE", "img": IMG_ICE}
BOMB_TYPE = {"name": "BOMB", "img": IMG_BOMB}
GOLDENFRUIT_TYPE = {"name": "GOLDENFRUIT", "img": IMG_GOLDENFRUIT, "img_slice": IMG_GOLDENFRUIT_SLICE, "bonus_points": 5}


# === CLASSE OBJET ===
class FallingObject:
    def __init__(self, obj_type, x, y, vy, vx=0.0, is_slice=False):
        self.type = obj_type
        self.image = obj_type["img"]
        self.rect = self.image.get_rect(center=(x, y))
        self.vy = vy
        self.vx = vx
        self.is_slice = is_slice
        self.spawn_time = pygame.time.get_ticks()
        self.bomb_timer = 2500

    def draw(self, surface):
        if self.type is BOMB_TYPE:
            elapsed = pygame.time.get_ticks() - self.spawn_time
            if elapsed > 1500 and (elapsed // 150) % 2 == 0:
                surface.blit(self.image, self.rect)
                pygame.draw.circle(surface, (255, 0, 0), self.rect.center, 35, 3)
            else:
                surface.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect)
    
    def is_bomb_expired(self):
        if self.type is BOMB_TYPE:
            return pygame.time.get_ticks() - self.spawn_time > self.bomb_timer
        return False


# === FONCTIONS DE SPAWN ===
def _random_spawn_bottom():
    x = random.randint(150, 650)
    y = 590
    vy = random.uniform(-0.65, -0.75)
    vx = random.uniform(-0.10, 0.10)
    return x, y, vy, vx


def random_fruit():
    t = random.choice(FRUIT_TYPES)
    x, y, vy, vx = _random_spawn_bottom()
    return FallingObject(t, x, y, vy, vx)


def ice_cube():
    x, y, vy, vx = _random_spawn_bottom()
    return FallingObject(ICE_TYPE, x, y, vy, vx)


def bomb():
    x, y, vy, vx = _random_spawn_bottom()
    return FallingObject(BOMB_TYPE, x, y, vy, vx)


def goldenfruit():
    x, y, vy, vx = _random_spawn_bottom()
    return FallingObject(GOLDENFRUIT_TYPE, x, y, vy, vx)


def make_slices_from_fruit(obj):
    """Crée les tranches après un slice"""
    slice_type = {"name": obj.type["name"] + "_SLICE", "img": obj.type["img_slice"]}
    x, y = obj.rect.center
    vy = obj.vy * 0.6
    
    if obj.type["name"] == "BANANA":
        return [FallingObject(slice_type, x, y, vy, vx=obj.vx, is_slice=True)]
    
    left = FallingObject(slice_type, x, y, vy, vx=obj.vx - 0.1, is_slice=True)
    right = FallingObject(slice_type, x, y, vy, vx=obj.vx + 0.1, is_slice=True)
    return [left, right]
