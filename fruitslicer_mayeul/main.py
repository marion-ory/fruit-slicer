import pygame
from screens import splash_screen, main_menu
from game_mouse import game_loop_mouse
from game_keyboard import game_loop_keyboard


def main():
    if not splash_screen():
        pygame.quit()
        return

    while True:
        action, mode, difficulty = main_menu()
        
        if action is None:
            break
        
        if action == "PLAY":
            if mode == "SOURIS":
                game_loop_mouse(difficulty)
            elif mode == "CLAVIER":
                game_loop_keyboard(difficulty)

    pygame.quit()


if __name__ == "__main__":
    main()
