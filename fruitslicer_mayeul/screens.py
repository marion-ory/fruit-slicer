import pygame
import json
import os
from config import *
from rendering import draw_text, blit_scaled, logical_mouse_pos

SCORES_FILE = os.path.join(BASE_DIR, "scores.json")


# === GESTION SCORES ===
def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_score(score):
    scores = load_scores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:10]
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f)


# === ÉCRANS ===
def splash_screen():
    """Écran de démarrage"""
    timer_start = pygame.time.get_ticks()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True
            if event.type == pygame.VIDEORESIZE:
                global WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        logo_rect = LOGO.get_rect(center=(LOGICAL_WIDTH // 2, LOGICAL_HEIGHT // 2))
        SCREEN.blit(LOGO, logo_rect)
        draw_text(SCREEN, "Appuie sur ENTER", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 80))
        
        blit_scaled(WINDOW, SCREEN)
        CLOCK.tick(FPS)
        
        if pygame.time.get_ticks() - timer_start > 4000:
            return True


def mode_screen():
    """Choix du mode de jeu"""
    modes = ["SOURIS", "CLAVIER"]
    selected = 0
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                mouse_pos = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    selected = (selected + 1) % len(modes)
                if event.key == pygame.K_RETURN:
                    return modes[selected]
            if event.type == pygame.VIDEORESIZE:
                global WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        mx, my = logical_mouse_pos(WINDOW, mouse_pos)
        
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        draw_text(SCREEN, "Choisis ton mode", FONT_BIG, WHITE, (LOGICAL_WIDTH // 2, 150))
        
        # Détecte quel élément est survolé par la souris
        hovered_index = None
        for i, mode in enumerate(modes):
            text_img = FONT_MED.render(mode, True, WHITE)
            text_rect = text_img.get_rect(center=(LOGICAL_WIDTH // 2, 230 + i * 60))
            
            # Vérifie si la souris est dessus
            if text_rect.collidepoint(mx, my):
                hovered_index = i
                if click:
                    return modes[i]
        
        # Affiche les options
        for i, mode in enumerate(modes):
            # JAUNE uniquement si survolé par la souris
            color = YELLOW if i == hovered_index else WHITE
            draw_text(SCREEN, mode, FONT_MED, color, (LOGICAL_WIDTH // 2, 230 + i * 60))
        
        draw_text(SCREEN, "ENTER pour valider, ESC pour annuler", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 60))
        
        blit_scaled(WINDOW, SCREEN)
        CLOCK.tick(FPS)


def difficulty_screen():
    """Choix de difficulté"""
    difficulties = ["EASY", "HARD"]
    selected = 0
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                mouse_pos = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    selected = (selected + 1) % len(difficulties)
                if event.key == pygame.K_RETURN:
                    return difficulties[selected]
            if event.type == pygame.VIDEORESIZE:
                global WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        mx, my = logical_mouse_pos(WINDOW, mouse_pos)
        
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        draw_text(SCREEN, "Choisis la difficulte", FONT_BIG, WHITE, (LOGICAL_WIDTH // 2, 150))
        
        # Détecte quel élément est survolé par la souris
        hovered_index = None
        for i, diff in enumerate(difficulties):
            text_img = FONT_MED.render(diff, True, WHITE)
            text_rect = text_img.get_rect(center=(LOGICAL_WIDTH // 2, 230 + i * 60))
            
            # Vérifie si la souris est dessus
            if text_rect.collidepoint(mx, my):
                hovered_index = i
                if click:
                    return difficulties[i]
        
        # Affiche les options
        for i, diff in enumerate(difficulties):
            # JAUNE uniquement si survolé par la souris
            color = YELLOW if i == hovered_index else WHITE
            draw_text(SCREEN, diff, FONT_MED, color, (LOGICAL_WIDTH // 2, 230 + i * 60))
        
        draw_text(SCREEN, "ENTER pour valider, ESC pour annuler", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 60))
        
        blit_scaled(WINDOW, SCREEN)
        CLOCK.tick(FPS)



def main_menu():
    """Menu principal"""
    buttons = [
        ("Jouer", (LOGICAL_WIDTH // 2, 260)),
        ("Tableau des scores", (LOGICAL_WIDTH // 2, 320)),
        ("Quitter", (LOGICAL_WIDTH // 2, 380)),
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None, None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                mouse_pos = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None, None
            if event.type == pygame.VIDEORESIZE:
                global WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        mx, my = logical_mouse_pos(WINDOW, mouse_pos)
        
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        draw_text(SCREEN, "Fruit Slicer", FONT_BIG, WHITE, (LOGICAL_WIDTH // 2, 150))
        
        for i, (label, center) in enumerate(buttons):
            rect = pygame.Rect(0, 0, 320, 50)
            rect.center = center
            color = BLUE
            
            if rect.collidepoint(mx, my):
                color = YELLOW
                if click:
                    if i == 0:
                        mode = mode_screen()
                        if mode is None:
                            continue
                        difficulty = difficulty_screen()
                        if difficulty is not None:
                            return "PLAY", mode, difficulty
                    elif i == 1:
                        scores_screen()
                    elif i == 2:
                        return None, None, None
            
            pygame.draw.rect(SCREEN, color, rect)
            draw_text(SCREEN, label, FONT_MED, BLACK, rect.center)
        
        blit_scaled(WINDOW, SCREEN)
        CLOCK.tick(FPS)


def scores_screen():
    """Tableau des scores"""
    scores = load_scores()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return
            if event.type == pygame.VIDEORESIZE:
                global WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        draw_text(SCREEN, "Scores", FONT_BIG, WHITE, (LOGICAL_WIDTH // 2, 120))
        
        y = 200
        for i, s in enumerate(scores[:5], start=1):
            draw_text(SCREEN, f"{i}. {s}", FONT_MED, WHITE, (LOGICAL_WIDTH // 2, y))
            y += 40
        
        if not scores:
            draw_text(SCREEN, "Aucun score", FONT_MED, WHITE, (LOGICAL_WIDTH // 2, 260))
        
        draw_text(SCREEN, "ENTER ou ESC pour revenir", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 60))
        
        blit_scaled(WINDOW, SCREEN)
        CLOCK.tick(30)


def game_over_screen(score):
    """Écran game over"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return
            if event.type == pygame.VIDEORESIZE:
                global WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        SCREEN.fill(BLACK)
        draw_text(SCREEN, "Game Over", FONT_BIG, RED, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT // 3))
        draw_text(SCREEN, f"Score : {score}", FONT_MED, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT // 2))
        draw_text(SCREEN, "ENTER / ESC pour revenir", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT * 2 // 3))
        
        blit_scaled(WINDOW, SCREEN)
        CLOCK.tick(30)
