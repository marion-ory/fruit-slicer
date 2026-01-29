import pygame
from config import LOGICAL_WIDTH, LOGICAL_HEIGHT


def draw_text(surface, text, font, color, center):
    """Dessine du texte centré"""
    img = font.render(text, True, color)
    rect = img.get_rect(center=center)
    surface.blit(img, rect)


def draw_sword_trail(surface, points):
    """Dessine la trainée de souris avec effet de fondu"""
    if len(points) < 2:
        return
    
    trail_surface = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT), pygame.SRCALPHA)
    
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        t = i / (len(points) - 1)
        width = int(12 * (1 - t) + 2 * t)
        alpha = int(220 * (1 - t))
        color = (255, 255, 255, alpha)
        pygame.draw.line(trail_surface, color, p1, p2, width)
    
    surface.blit(trail_surface, (0, 0))


def blit_scaled(window, screen):
    """Affiche l'écran logique sur la fenêtre redimensionnable"""
    win_w, win_h = window.get_size()
    scaled = pygame.transform.smoothscale(screen, (win_w, win_h))
    window.blit(scaled, (0, 0))
    pygame.display.flip()


def logical_mouse_pos(window, real_pos):
    """Convertit position souris réelle en coordonnées logiques"""
    win_w, win_h = window.get_size()
    rx = real_pos[0] / win_w
    ry = real_pos[1] / win_h
    return int(rx * LOGICAL_WIDTH), int(ry * LOGICAL_HEIGHT)
