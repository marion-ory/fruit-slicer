# physics.py

from config import LOGICAL_HEIGHT, COMBO_WINDOW_MS
from entities import FRUIT_TYPES, ICE_TYPE, BOMB_TYPE, GOLDENFRUIT_TYPE, make_slices_from_fruit

GRAVITY = 0.0006

def apply_gravity_and_move(obj, dt, speed_multiplier=1.0, slow_motion=False):
    # Ralentissement en slow-motion
    if slow_motion:
        dt *= 0.3  # 30% de la vitesse normale
    
    obj.vy += GRAVITY * dt * speed_multiplier
    obj.rect.y += obj.vy * dt
    obj.rect.x += obj.vx * dt

def is_off_screen(obj):
    return obj.rect.top > LOGICAL_HEIGHT + 80 or obj.rect.right < -80 or obj.rect.left > 880

def handle_key_press(key, objects, now_ms, last_hit_times, combo_multiplier):
    hit = False
    score_gain = 0
    bomb_triggered = False
    freeze_triggered = False
    wrong_key_pressed = False
    bomb_defused = False
    
    # Vérifie si la touche correspond à un objet à l'écran
    valid_keys = [obj.key for obj in objects if obj.key is not None]
    
    touched = [obj for obj in objects if obj.key == key]
    
    # Pénalité si touche pressée sans objet correspondant
    if key in [pygame.K_a, pygame.K_b, pygame.K_o, pygame.K_g] and not touched:
        wrong_key_pressed = True
        return False, -2, False, False, True, False  # -2 points de pénalité
    
    if not touched:
        return False, 0, False, False, False, False
    
    new_objects = []
    for obj in touched:
        hit = True
        if obj.type in FRUIT_TYPES:
            base_points = obj.type["base_points"]
            score_gain += base_points * combo_multiplier
            new_objects.extend(make_slices_from_fruit(obj))
        elif obj.type is ICE_TYPE:
            freeze_triggered = True
            score_gain += 3  # Bonus pour avoir pris le glaçon
        elif obj.type is BOMB_TYPE:
            # Si on appuie sur X sur une bombe, on la désactive
            bomb_defused = True
            score_gain += 2  # Petit bonus pour avoir désactivé
        elif obj.type is GOLDENFRUIT_TYPE:
            score_gain += obj.type["bonus_points"] * combo_multiplier
        objects.remove(obj)
    
    objects.extend(new_objects)
    
    if hit and not bomb_defused:
        last_hit_times.append(now_ms)
        last_hit_times[:] = [t for t in last_hit_times if now_ms - t <= COMBO_WINDOW_MS]
    
    return hit, score_gain, bomb_triggered, freeze_triggered, wrong_key_pressed, bomb_defused

import pygame
