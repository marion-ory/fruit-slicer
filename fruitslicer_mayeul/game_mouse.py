import pygame
from config import *
from entities import FRUIT_TYPES, ICE_TYPE, BOMB_TYPE, GOLDENFRUIT_TYPE, make_slices_from_fruit
from spawner import BeatSpawner
from physics import apply_gravity_and_move, is_off_screen
from audio_analysis import analyze_music
from rendering import draw_text, draw_sword_trail, blit_scaled, logical_mouse_pos
from screens import game_over_screen, save_score
from sounds import play_fruit_sound, play_golden_sound, play_bomb_sound, play_combo_sound, start_music, stop_music


def segment_intersects_rect(p1, p2, rect):
    """Vérifie si le segment souris touche un rectangle"""
    if rect.collidepoint(p1) or rect.collidepoint(p2):
        return True
    
    r = rect
    rect_segments = [
        ((r.left, r.top), (r.right, r.top)),
        ((r.right, r.top), (r.right, r.bottom)),
        ((r.right, r.bottom), (r.left, r.bottom)),
        ((r.left, r.bottom), (r.left, r.top)),
    ]
    
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    def segments_intersect(A, B, C, D):
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
    
    for a, b in rect_segments:
        if segments_intersect(p1, p2, a, b):
            return True
    return False


def game_loop_mouse(difficulty):
    """Boucle de jeu mode SOURIS"""
    bpm, beat_times_ms = analyze_music()
    spawner = BeatSpawner(beat_times_ms, difficulty=difficulty)
    speed_multiplier = DIFFICULTY_SETTINGS[difficulty]["speed_multiplier"]
    
    start_music()
    
    objects = []
    score = 0
    lives = 3
    freeze_active = False
    freeze_end_time = 0
    combo_count = 0
    combo_active = False
    mouse_path = []
    last_mouse_pos = None
    start_ticks = pygame.time.get_ticks()
    
    while True:
        dt = CLOCK.tick(FPS)
        now_ms = pygame.time.get_ticks()
        elapsed_ms = now_ms - start_ticks
        
        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                stop_music()
                return
            if event.type == pygame.VIDEORESIZE:
                global WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        # Souris
        real_mouse = pygame.mouse.get_pos()
        mx, my = logical_mouse_pos(WINDOW, real_mouse)
        
        if last_mouse_pos is None:
            last_mouse_pos = (mx, my)
        
        mouse_segment = (last_mouse_pos, (mx, my))
        last_mouse_pos = (mx, my)
        
        mouse_path.append((mx, my))
        if len(mouse_path) > 25:
            mouse_path.pop(0)
        
        # Détection slices
        gain = 0
        bomb_trig = False
        freeze_trig = False
        new_objects = []
        just_activated_combo = False
        
        for obj in list(objects):
            if segment_intersects_rect(*mouse_segment, obj.rect):
                
                if obj.type in FRUIT_TYPES:
                    points = 3 if combo_active else 1
                    gain += points
                    combo_count += 1
                    play_fruit_sound()
                    
                    if combo_count >= 10 and not combo_active:
                        combo_active = True
                        just_activated_combo = True
                    
                    new_objects.extend(make_slices_from_fruit(obj))
                    objects.remove(obj)
                
                elif obj.type is ICE_TYPE:
                    freeze_trig = True
                    objects.remove(obj)
                
                elif obj.type is BOMB_TYPE:
                    bomb_trig = True
                    play_bomb_sound()
                    objects.remove(obj)
                
                elif obj.type is GOLDENFRUIT_TYPE:
                    points = 15 if combo_active else 5
                    gain += points
                    combo_count += 1
                    play_golden_sound()
                    
                    if lives < 5:
                        lives += 1
                    
                    if combo_count >= 10 and not combo_active:
                        combo_active = True
                        just_activated_combo = True
                    
                    new_objects.extend(make_slices_from_fruit(obj))
                    objects.remove(obj)
        
        if just_activated_combo:
            play_combo_sound()
        
        objects.extend(new_objects)
        score = max(0, score + gain)
        
        if bomb_trig:
            lives -= 2
            combo_count = 0
            combo_active = False
            if lives <= 0:
                break
        
        if freeze_trig:
            freeze_active = True
            freeze_end_time = now_ms + FREEZE_DURATION_MS
        
        if freeze_active and now_ms > freeze_end_time:
            freeze_active = False
        
        spawner.update(elapsed_ms, objects)
        
        for obj in list(objects):
            apply_gravity_and_move(obj, dt, speed_multiplier=speed_multiplier, slow_motion=freeze_active)
            
            if is_off_screen(obj):
                if obj.type in FRUIT_TYPES and elapsed_ms > 8000 and not obj.is_slice:
                    lives -= 1
                    combo_count = 0
                    combo_active = False
                    if lives <= 0:
                        break
                objects.remove(obj)
        
        if lives <= 0:
            break
        
        # Affichage
        SCREEN.blit(BACKGROUND_GAME, (0, 0))
        
        for obj in objects:
            obj.draw(SCREEN)
        
        draw_sword_trail(SCREEN, mouse_path)
        
        multiplier_text = " (x3)" if combo_active else ""
        draw_text(SCREEN, f"Score: {score}{multiplier_text}", FONT_MED, YELLOW if combo_active else WHITE, (150, 40))
        
        combo_text = f"COMBO x3! ({combo_count})" if combo_active else f"Combo: {combo_count}/10"
        draw_text(SCREEN, combo_text, FONT_MED, ORANGE if combo_active else WHITE, (LOGICAL_WIDTH // 2, 40))
        
        for i in range(min(lives, 5)):
            SCREEN.blit(IMG_HEART, (LOGICAL_WIDTH - 40 - i * 40, 20))
        
        if freeze_active:
            draw_text(SCREEN, "SLOW MOTION!", FONT_MED, BLUE, (LOGICAL_WIDTH // 2, 100))
        
        if combo_active:
            SCREEN.blit(IMG_COMBO, (LOGICAL_WIDTH // 2 - IMG_COMBO.get_width() // 2, LOGICAL_HEIGHT // 2 - 100))
        
        blit_scaled(WINDOW, SCREEN)
    
    stop_music()
    save_score(score)
    game_over_screen(score)
