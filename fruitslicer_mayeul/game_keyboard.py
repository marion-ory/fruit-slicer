import pygame
from config import *
from entities import FRUIT_TYPES, ICE_TYPE, BOMB_TYPE, GOLDENFRUIT_TYPE, make_slices_from_fruit
from spawner import BeatSpawner
from physics import apply_gravity_and_move, is_off_screen
from audio_analysis import analyze_music
from rendering import draw_text, blit_scaled
from screens import game_over_screen, save_score
from sounds import play_fruit_sound, play_golden_sound, play_bomb_sound, play_combo_sound, start_music, stop_music


def find_closest_fruit_by_type(objects, fruit_name):
    """Trouve le fruit du type spécifié le plus proche du centre"""
    center_x = LOGICAL_WIDTH // 2
    center_y = LOGICAL_HEIGHT // 2
    
    closest_obj = None
    min_distance = float('inf')
    
    for obj in objects:
        # Vérifie le type
        if obj.type["name"] == fruit_name:
            dx = obj.rect.centerx - center_x
            dy = obj.rect.centery - center_y
            distance = (dx**2 + dy**2) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                closest_obj = obj
    
    return closest_obj


def game_loop_keyboard(difficulty):
    """Boucle de jeu mode CLAVIER"""
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
    keys_pressed = set()
    start_ticks = pygame.time.get_ticks()
    
    # MAPPING TOUCHES → FRUITS
    key_to_fruit = {
        pygame.K_a: "APPLE",
        pygame.K_b: "BANANA",
        pygame.K_o: "ORANGE",
        pygame.K_s: "GOLDENFRUIT",
        pygame.K_i: "ICE",
    }
    
    while True:
        dt = CLOCK.tick(FPS)
        now_ms = pygame.time.get_ticks()
        elapsed_ms = now_ms - start_ticks
        
        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_music()
                    return
                keys_pressed.add(event.key)
            if event.type == pygame.KEYUP:
                keys_pressed.discard(event.key)
            if event.type == pygame.VIDEORESIZE:
                global WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        # Détection
        gain = 0
        freeze_trig = False
        new_objects = []
        just_activated_combo = False
        
        # === GESTION DES TOUCHES FRUITS ===
        for key, fruit_name in key_to_fruit.items():
            if key in keys_pressed:
                keys_pressed.discard(key)
                
                # Trouve le fruit de ce type le plus proche
                closest_obj = find_closest_fruit_by_type(objects, fruit_name)
                
                if closest_obj:
                    # FRUIT NORMAL (pomme, banane, orange)
                    if closest_obj.type in FRUIT_TYPES:
                        points = 3 if combo_active else 1
                        gain += points
                        combo_count += 1
                        play_fruit_sound()
                        
                        if combo_count >= 10 and not combo_active:
                            combo_active = True
                            just_activated_combo = True
                        
                        new_objects.extend(make_slices_from_fruit(closest_obj))
                        objects.remove(closest_obj)
                    
                    # FRUIT DORÉ
                    elif closest_obj.type is GOLDENFRUIT_TYPE:
                        points = 15 if combo_active else 5
                        gain += points
                        combo_count += 1
                        play_golden_sound()
                        
                        if lives < 5:
                            lives += 1
                        
                        if combo_count >= 10 and not combo_active:
                            combo_active = True
                            just_activated_combo = True
                        
                        new_objects.extend(make_slices_from_fruit(closest_obj))
                        objects.remove(closest_obj)
                    
                    # ICE
                    elif closest_obj.type is ICE_TYPE:
                        freeze_trig = True
                        objects.remove(closest_obj)
        
        # === ESPACE → DÉSACTIVE BOMBE ===
        if pygame.K_SPACE in keys_pressed:
            keys_pressed.discard(pygame.K_SPACE)
            
            # Trouve la bombe la plus proche
            center_x = LOGICAL_WIDTH // 2
            center_y = LOGICAL_HEIGHT // 2
            closest_bomb = None
            min_distance = float('inf')
            
            for obj in objects:
                if obj.type is BOMB_TYPE:
                    dx = obj.rect.centerx - center_x
                    dy = obj.rect.centery - center_y
                    distance = (dx**2 + dy**2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        closest_bomb = obj
            
            if closest_bomb:
                objects.remove(closest_bomb)
                gain += 2
        
        if just_activated_combo:
            play_combo_sound()
        
        objects.extend(new_objects)
        score = max(0, score + gain)
        
        if freeze_trig:
            freeze_active = True
            freeze_end_time = now_ms + FREEZE_DURATION_MS
        
        if freeze_active and now_ms > freeze_end_time:
            freeze_active = False
        
        spawner.update(elapsed_ms, objects)
        
        for obj in list(objects):
            apply_gravity_and_move(obj, dt, speed_multiplier=speed_multiplier, slow_motion=freeze_active)
            
            # Bombe explose
            if obj.type is BOMB_TYPE and obj.is_bomb_expired():
                play_bomb_sound()
                lives -= 1
                combo_count = 0
                combo_active = False
                objects.remove(obj)
                if lives <= 0:
                    break
            
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
        
        # Instructions clavier
        draw_text(SCREEN, "A=Pomme B=Banane O=Orange S=Dore I=Glace ESPACE=Bombe", 
                  FONT_SMALL, WHITE, (LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 40))
        
        multiplier_text = " (x3)" if combo_active else ""
        draw_text(SCREEN, f"Score: {score}{multiplier_text}", FONT_MED, 
                  YELLOW if combo_active else WHITE, (150, 40))
        
        combo_text = f"COMBO x3! ({combo_count})" if combo_active else f"Combo: {combo_count}/10"
        draw_text(SCREEN, combo_text, FONT_MED, ORANGE if combo_active else WHITE, 
                  (LOGICAL_WIDTH // 2, 40))
        
        for i in range(min(lives, 5)):
            SCREEN.blit(IMG_HEART, (LOGICAL_WIDTH - 40 - i * 40, 20))
        
        if freeze_active:
            draw_text(SCREEN, "SLOW MOTION!", FONT_MED, BLUE, (LOGICAL_WIDTH // 2, 100))
        
        if combo_active:
            SCREEN.blit(IMG_COMBO, (LOGICAL_WIDTH // 2 - IMG_COMBO.get_width() // 2, 
                                   LOGICAL_HEIGHT // 2 - 100))
        
        blit_scaled(WINDOW, SCREEN)
    
    stop_music()
    save_score(score)
    game_over_screen(score)
