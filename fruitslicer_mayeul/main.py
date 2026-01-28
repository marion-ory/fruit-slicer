# main.py
import pygame
from game import splash_screen, main_menu, game_loop

def main():
    if not splash_screen():
        pygame.quit()
        return

    running = True
    while running:
        action, difficulty = main_menu()
        if action is None:
            running = False
        elif action == "PLAY":
            game_loop(difficulty)

    pygame.quit()

if __name__ == "__main__":
    main()
