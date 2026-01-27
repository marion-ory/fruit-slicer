import random
from models import Fructs, Bomb, Ice


class GameEngine:
    def __init__(self):
        self.active_objects = []
        # lives & score
        self.score = 0
        self.strikes = 0
        self.is_GameOver = False
        # ICE
        self.is_frozen = False
        self.FreezeTimer = 0
        # timmer level
        self.spawn_timer = 0
        self.spawn_delay = 60  #

        self.fructs_type = ["pomme", "banane", "orange", "fruit d'or"]


def update(self):
    for object in self.active_objects[:]:
        if not self.is_frozen:
            object.move()

        if object.is_sliced:  # LOGIC IS SLICED
            if isinstance(object, Ice):
                self.is_frozen = True
                self.FreezeTimer = 180
                print(f"FREEZE {self.FreezeTimer}")

            elif isinstance(object, Bomb):
                self.is_GameOver = True
                print(f"GAME OVER {self.is_GameOver}")

            elif isinstance(object, Fructs):
                self.score += 1
                print(f"Bravo ! {self.score}")
            self.active_objects.remove(object)
            continue

        if object.y > 600:  # LOGIC IS OUT OF SCREEN
            if isinstance(object, Fructs) and not object.is_sliced:
                self.strikes += 1
                print(f"Raté ! Strikes : {self.strikes} / 3")
                if self.strikes >= 3:
                    self.is_GameOver = True
                print(f"Game Over: {self.is_GameOver} ")

            if object in self.active_objects:
                self.active_objects.remove(object)

    if object.is_frozen:  # LOGIC TIMER FREEZE
        self.FreezeTimer -= 1
        if self.FreezeTimer > 0:
            self.is_Frozen = False  # restart frozen timer

    self.spawn_timer += 1  # apparition random object each 60scd
    if self.spawn_timer >= self.span_delay:
        self.spawner()
        self.spawn_timer = 0


# Object generator place with random
def spawner(self):
    type = ["fruct", "bomb", "ice"]
    choose = random.choice(type)
    # position random
    x_random = random.randint(100, 700)
    y_start = 650  # under the screen (position)

    letter = "abcdefghijklmnopqrstuvwxyz"
    letter_choice = random.choice(letter)

    if choose == "fruct":
        name_random = random.choice(self.fructs_type)
        new_object = Fructs(name=name_random, x=x_random, y=y_start, key=letter_choice)
    elif choose == "bomb":
        new_object = Bomb(name="bomb", x=x_random, y=y_start, key=letter_choice)
    else:
        new_object == Ice(name="ice", x=x_random, y=y_start, key=letter_choice)

    self.active_objects.append(new_object)
