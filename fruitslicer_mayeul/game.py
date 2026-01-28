# game.py

import pygame
import json
import os
from config import WINDOW, SCREEN, CLOCK, FPS
from config import LOGICAL_WIDTH, LOGICAL_HEIGHT
from config import BACKGROUND_MENU, BACKGROUND_GAME, LOGO
from config import WHITE, BLACK, RED, BLUE, GREEN, YELLOW, ORANGE
from config import FONT_BIG, FONT_MED, FONT_SMALL
from config import IMG_HEART, IMG_COMBO, FREEZE_DURATION_MS
from config import DIFFICULTY_SETTINGS, MUSIC_FILE, BASE_DIR
from config import COMBO_WINDOW_MS, COMBO_MULTIPLIERS, COMBO_FOR_LIFE
from entities import FRUIT_TYPES, BOMB_TYPE
from spawner import BeatSpawner
from physics import apply_gravity_and_move, is_off_screen, handle_key_press
from audio_analysis import analyze_music

SCORES_FILE = os.path.join(BASE_DIR, "scores.json")

def draw_text(surface, text, font, color, center):
    img = font.render(text, True, color)
    rect = img.get_rect(center=center)
    surface.blit(img, rect)

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

def resize_window(new_w, new_h):
    global WINDOW
    WINDOW = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)

def blit_scaled():
    win_w, win_h = WINDOW.get_size()
    scaled = pygame.transform.smoothscale(SCREEN, (win_w, win_h))
    WINDOW.blit(scaled, (0, 0))
    pygame.display.flip()

def logical_mouse_pos(real_pos):
    win_w, win_h = WINDOW.get_size()
    rx = real_pos[0] / win_w
    ry = real_pos[1] / win_h
    return int(rx * LOGICAL_WIDTH), int(ry * LOGICAL_HEIGHT)

def splash_screen():
    running = True
    timer_start = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True
            if event.type == pygame.VIDEORESIZE:
                resize_window(event.w, event.h)
        
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        logo_rect = LOGO.get_rect(center=(LOGICAL_WIDTH // 2, LOGICAL_HEIGHT // 2))
        SCREEN.blit(LOGO, logo_rect)
        draw_text(SCREEN, "Appuie sur ENTER", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 80))
        
        blit_scaled()
        CLOCK.tick(FPS)
        
        if pygame.time.get_ticks() - timer_start > 4000:
            return True

def difficulty_screen():
    difficulties = ["EASY", "HARD"]
    selected = 0
    selecting = True
    
    while selecting:
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
                resize_window(event.w, event.h)
        
        mx, my = logical_mouse_pos(mouse_pos)
        
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        draw_text(SCREEN, "Choisis la difficulté", FONT_BIG, WHITE, (LOGICAL_WIDTH // 2, 150))
        
        for i, diff in enumerate(difficulties):
            color = YELLOW if i == selected else WHITE
            draw_text(SCREEN, diff, FONT_MED, color, (LOGICAL_WIDTH // 2, 230 + i * 60))
        
        for i, diff in enumerate(difficulties):
            text_img = FONT_MED.render(diff, True, WHITE)
            text_rect = text_img.get_rect(center=(LOGICAL_WIDTH // 2, 230 + i * 60))
            if text_rect.collidepoint(mx, my) and click:
                return difficulties[i]
        
        draw_text(SCREEN, "ENTER pour valider, ESC pour annuler", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 60))
        
        blit_scaled()
        CLOCK.tick(FPS)

def main_menu():
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
                return None, None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                mouse_pos = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None
            if event.type == pygame.VIDEORESIZE:
                resize_window(event.w, event.h)
        
        mx, my = logical_mouse_pos(mouse_pos)
        
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
                        difficulty = difficulty_screen()
                        if difficulty is not None:
                            return "PLAY", difficulty
                    elif i == 1:
                        scores_screen()
                    elif i == 2:
                        return None, None
            
            pygame.draw.rect(SCREEN, color, rect)
            draw_text(SCREEN, label, FONT_MED, BLACK, rect.center)
        
        blit_scaled()
        CLOCK.tick(FPS)

def scores_screen():
    scores = load_scores()
    waiting = True
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    waiting = False
            if event.type == pygame.VIDEORESIZE:
                resize_window(event.w, event.h)
        
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        draw_text(SCREEN, "Scores", FONT_BIG, WHITE, (LOGICAL_WIDTH // 2, 120))
        
        y = 200
        for i, s in enumerate(scores[:5], start=1):
            draw_text(SCREEN, f"{i}. {s}", FONT_MED, WHITE, (LOGICAL_WIDTH // 2, y))
            y += 40
        
        if not scores:
            draw_text(SCREEN, "Aucun score pour l'instant", FONT_MED, WHITE, (LOGICAL_WIDTH // 2, 260))
        
        draw_text(SCREEN, "ENTER ou ESC pour revenir", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 60))
        
        blit_scaled()
        CLOCK.tick(30)

def get_combo_multiplier(combo_count):
    """Retourne le multiplicateur basé sur le nombre de combos"""
    for threshold in sorted(COMBO_MULTIPLIERS.keys(), reverse=True):
        if combo_count >= threshold:
            return COMBO_MULTIPLIERS[threshold]
    return 1

def game_loop(difficulty):
    bpm, beat_times_ms = analyze_music()
    spawner = BeatSpawner(beat_times_ms, difficulty=difficulty)
    speed_multiplier = DIFFICULTY_SETTINGS[difficulty]["speed_multiplier"]
    
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.play()
    
    objects = []
    score = 0
    lives = 3
    
    freeze_active = False
    freeze_end_time = 0
    
    combo_count = 0
    combo_active = False
    combo_end_time = 0
    
    total_combo_hits = 0  # Pour le système de vie bonus
    
    last_hit_times = []
    
    start_ticks = pygame.time.get_ticks()
    MIN_GAME_TIME_MS = 8000
    
    running = True
    
    while running:
        dt = CLOCK.tick(FPS)
        now_ms = pygame.time.get_ticks()
        elapsed_ms = now_ms - start_ticks
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return
                
                combo_multiplier = get_combo_multiplier(combo_count)
                
                hit, gain, bomb_trig, freeze_trig, wrong_key, bomb_defused = handle_key_press(
                    event.key, objects, now_ms, last_hit_times, combo_multiplier
                )
                
                score = max(0, score + gain)  # Le score ne peut pas être négatif
                
                if wrong_key:
                    lives -= 1  # Pénalité pour mauvaise touche
                    if lives <= 0:
                        running = False
                        break
                
                if bomb_trig:
                    lives -= 2
                    if lives <= 0:
                        running = False
                        break
                
                if freeze_trig:
                    freeze_active = True
                    freeze_end_time = now_ms + FREEZE_DURATION_MS
                
                # Système de combo
                if hit and not bomb_defused:
                    combo_count = len(last_hit_times)
                    total_combo_hits += 1
                    
                    # Gagner une vie tous les 15 hits en combo
                    if total_combo_hits % COMBO_FOR_LIFE == 0 and lives < 5:
                        lives += 1
                    
                    if combo_count >= 3:
                        combo_active = True
                        combo_end_time = now_ms + 800
            
            if event.type == pygame.VIDEORESIZE:
                resize_window(event.w, event.h)
        
        # Désactiver le freeze
        if freeze_active and now_ms > freeze_end_time:
            freeze_active = False
        
        # Désactiver l'affichage combo
        if combo_active and now_ms > combo_end_time:
            combo_active = False
        
        # Reset combo si trop de temps
        if last_hit_times:
            if now_ms - last_hit_times[-1] > COMBO_WINDOW_MS:
                combo_count = 0
        
        # Vérifier les bombes expirées
        for obj in list(objects):
            if obj.is_bomb_expired():
                lives -= 1
                objects.remove(obj)
                if lives <= 0:
                    running = False
                    break
        
        spawner.update(elapsed_ms, objects)
        
        for obj in list(objects):
            apply_gravity_and_move(obj, dt, speed_multiplier=speed_multiplier, slow_motion=freeze_active)
            
            if is_off_screen(obj):
                # Perdre une vie si un fruit tombe
                if obj.type in FRUIT_TYPES and elapsed_ms > MIN_GAME_TIME_MS and not obj.is_slice:
                    lives -= 1
                    if lives <= 0:
                        running = False
                        break
                objects.remove(obj)
        
        # Affichage
        SCREEN.blit(BACKGROUND_GAME, (0, 0))
        
        for obj in objects:
            obj.draw(SCREEN)
        
        # Score et multiplicateur
        multiplier = get_combo_multiplier(combo_count)
        score_text = f"Score: {score}"
        if multiplier > 1:
            score_text += f" (x{multiplier})"
        draw_text(SCREEN, score_text, FONT_MED, WHITE, (150, 40))
        
        # Vies
        for i in range(min(lives, 5)):
            x = LOGICAL_WIDTH - 40 - i * 40
            y = 20
            SCREEN.blit(IMG_HEART, (x, y))
        
        # Indicateur slow-motion
        if freeze_active:
            draw_text(SCREEN, "SLOW MOTION!", FONT_MED, BLUE, (LOGICAL_WIDTH // 2, 70))
            # Ralentir la musique
            if pygame.mixer.music.get_busy():
                pass  # Note: pygame.mixer ne supporte pas le pitch shift facilement
        
        # Indicateur combo
        if combo_active:
            SCREEN.blit(IMG_COMBO, (LOGICAL_WIDTH // 2 - IMG_COMBO.get_width() // 2, LOGICAL_HEIGHT // 2 - 80))
            combo_text = f"COMBO x{multiplier}!"
            draw_text(SCREEN, combo_text, FONT_SMALL, ORANGE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT // 2 + 20))
        
        # Progression vers vie bonus
        progress_text = f"Combo: {total_combo_hits % COMBO_FOR_LIFE}/{COMBO_FOR_LIFE}"
        draw_text(SCREEN, progress_text, FONT_SMALL, GREEN, (LOGICAL_WIDTH // 2, 100))
        
        # Aide touches
        key_help = "A=Pomme B=Banane O=Orange I=Glace X=Désactiver bombe G=Golden"
        draw_text(SCREEN, key_help, FONT_SMALL, YELLOW, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 30))
        
        blit_scaled()
    
    pygame.mixer.music.stop()
    save_score(score)
    game_over_screen(score)

def game_over_screen(score):
    waiting = True
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    waiting = False
                    return
            if event.type == pygame.VIDEORESIZE:
                resize_window(event.w, event.h)
        
        SCREEN.fill(BLACK)
        draw_text(SCREEN, "Game Over", FONT_BIG, RED, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT // 3))
        draw_text(SCREEN, f"Score : {score}", FONT_MED, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT // 2))
        draw_text(SCREEN, "ENTER / ESC pour revenir au menu", FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT * 2 // 3))
        
        blit_scaled()
        CLOCK.tick(30)
