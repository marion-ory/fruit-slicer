import random
from models import Fructs, Bomb, Ice, GoldenFruct


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
        # radom keydown, random fructs
        self.fructs_type = ["pomme", "banane", "orange", "fruit d'or"]
        self.available_keys = "abcdefghijklmnopqrstuvwxyz"
        # combo
        self.combo = 0
        self.multiplicateur = 1
        self.max_combo = 0

    def update(self):
        if self.is_frozen:  # LOGIC TIMER FREEZE
            self.FreezeTimer -= 1
            if self.FreezeTimer <= 0:
                self.is_frozen = False  # restart frozen timer

        self.spawn_timer += 1  # apparition random object each 60scd

        if self.spawn_timer >= self.spawn_delay:
            self.spawner()
            self.spawn_timer = 0

        for object in self.active_objects[:]:
            if not self.is_frozen:
                object.move()

            if object.is_sliced:  # LOGIC IS SLICED
                if isinstance(object, Ice):
                    self.is_frozen = True
                    self.FreezeTimer = 180
                    self.combo = 0
                    print(f"FREEZE {self.FreezeTimer}")

                elif isinstance(object, Bomb):
                    self.is_GameOver = True
                    self.combo = 0
                    print(f"GAME OVER {self.is_GameOver}")

                elif isinstance(object, Fructs):
                    self.score += object.points * self.multiplicateur
                    self.combo += 1
                    if self.combo > self.max_combo:
                        self.max_combo = self.combo
                    print(f"Bravo ! {self.score}")

                self.active_objects.remove(object)
                continue

            if object.y > 600:  # LOGIC IS OUT OF SCREEN
                if isinstance(object, Fructs) and not object.is_sliced:
                    self.strikes += 1
                    print(f"Raté ! Strikes : {self.strikes} / 3")
                    if self.strikes >= 3:
                        self.is_GameOver = True
                        self.combo = 0
                    print(f"Game Over: {self.is_GameOver} ")

                if object in self.active_objects:
                    self.active_objects.remove(object)

    # Object generator placement with random
    def spawner(self):
        # 1. Préparation des données communes
        x_random = random.randint(100, 700)
        y_start = 650
        random_key = random.choice(self.available_keys)

        # 2. Choix du type d'objet
        category = random.choice(["fruct", "bomb", "ice"])

        # 3. Création de l'objet (Logique simplifiée)
        if category == "fruct":
            name = random.choice(self.fructs_type)
            if name == "fruit d'or":
                new_object = GoldenFruct(x=x_random, y=y_start, key=random_key)
            else:
                new_object = Fructs(
                    name=name, points=2, x=x_random, y=y_start, key=random_key
                )

        elif category == "bomb":
            new_object = Bomb(x=x_random, y=y_start, key=random_key)

        else:  # Ice
            new_object = Ice(x=x_random, y=y_start, key=random_key)

        self.active_objects.append(new_object)

    # Collision object slice :
    def check_collision(self, key_pressed):
        for obj in self.active_objects:
            # Si la touche correspond et que l'objet n'est pas déjà tranché
            if obj.key == key_pressed and not obj.is_sliced:
                obj.is_sliced = True
                # On sort de la boucle pour ne pas trancher deux fruits
                # qui auraient la même touche par erreur
                return
