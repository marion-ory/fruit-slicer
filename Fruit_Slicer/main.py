import pygame
import sys  # Import indispensable pour sys.exit()
from engine import GameEngine

# 1. INITIALISATION
pygame.init()

# On définit WIDTH et HEIGHT pour pouvoir les utiliser partout
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slicer - Keyboard Ninja")

# INITIALISATION DES POLICES (C'était ça qui manquait !)
# On crée des objets Font pour pouvoir écrire du texte
pygame.font.init()
font_score = pygame.font.SysFont("Arial", 30, bold=True)
font_keys = pygame.font.SysFont("Arial", 24, bold=True)

engine = GameEngine()
clock = pygame.time.Clock()
running = True

# 2. BOUCLE DE JEU
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Détection des touches du clavier
        if event.type == pygame.KEYDOWN and not engine.is_GameOver:
            key_name = pygame.key.name(event.key)
            engine.check_collision(key_name)

    # B. MISE À JOUR (Logique)
    if not engine.is_GameOver:
        engine.update()

    # C. AFFICHAGE (Dessin)
    screen.fill((40, 44, 52))  # Fond sombre

    if not engine.is_GameOver:
        # On dessine les objets actifs
        for obj in engine.active_objects:
            # Choix de la couleur
            color = (255, 215, 0) if obj.name == "fruit d'or" else (200, 50, 50)
            if obj.name == "BOMBE":
                color = (20, 20, 20)
            if obj.name == "ICE_CUBE":
                color = (100, 200, 255)

            # Dessin du cercle
            pygame.draw.circle(screen, color, (int(obj.x), int(obj.y)), 30)

            # Dessin de la lettre (Render crée une surface de texte)
            key_surface = font_keys.render(obj.key.upper(), True, (255, 255, 255))
            screen.blit(key_surface, (obj.x - 10, obj.y - 15))

        # Affichage du Score et des Strikes
        score_text = font_score.render(
            f"Score: {engine.score}  Combo: x{engine.combo}", True, (255, 255, 255)
        )
        # On utilise WIDTH que l'on a défini en haut
        strikes_text = font_score.render(
            f"Strikes: {'X' * engine.strikes}", True, (255, 50, 50)
        )

        screen.blit(score_text, (20, 20))
        screen.blit(strikes_text, (WIDTH - 180, 20))

    else:
        # ÉCRAN DE GAME OVER
        game_over_surface = font_score.render("GAME OVER", True, (255, 0, 0))
        final_score = font_score.render(
            f"Score Final: {engine.score} | Max Combo: {engine.max_combo}",
            True,
            (255, 255, 255),
        )
        # Centrage du texte avec WIDTH et HEIGHT
        screen.blit(game_over_surface, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
        screen.blit(final_score, (WIDTH // 2 - 180, HEIGHT // 2 + 20))

    # D. RAFRAÎCHISSEMENT
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
