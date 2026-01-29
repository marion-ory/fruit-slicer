from config import LOGICAL_HEIGHT

GRAVITY = 0.0006


def apply_gravity_and_move(obj, dt, speed_multiplier=1.0, slow_motion=False):
    """Applique la gravité et déplace l'objet"""
    if slow_motion:
        dt *= 0.3
    
    obj.vy += GRAVITY * dt * speed_multiplier
    obj.rect.y += obj.vy * dt
    obj.rect.x += obj.vx * dt


def is_off_screen(obj):
    """Vérifie si l'objet est sorti de l'écran"""
    return obj.rect.top > LOGICAL_HEIGHT + 80 or obj.rect.right < -80 or obj.rect.left > 880
