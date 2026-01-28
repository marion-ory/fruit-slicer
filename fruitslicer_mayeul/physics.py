# physics.py

from config import LOGICAL_HEIGHT, COMBO_WINDOW_MS
from entities import FRUIT_TYPES, ICE_TYPE, BOMB_TYPE, GOLDENFRUIT_TYPE, make_slices_from_fruit

GRAVITY = 0.0006

def apply_gravity_and_move(obj, dt, speed_multiplier=1.0, slow_motion=False):
    if slow_motion:
        dt *= 0.3
    
    obj.vy += GRAVITY * dt * speed_multiplier
    obj.rect.y += obj.vy * dt
    obj.rect.x += obj.vx * dt

def is_off_screen(obj):
    return obj.rect.top > LOGICAL_HEIGHT + 80 or obj.rect.right < -80 or obj.rect.left > 880

import pygame
