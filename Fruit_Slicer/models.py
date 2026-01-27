import random
from constants import GRAVITY


# CLASS PARENTS
class GameObject:
    def __init__(self, name, points):
        self.name = name
        self.points = points

    # POSITION X,Y


self.x = random.randint(100, 700)
self.y = 600  # Part du bas de l'écran

# VITESSE vx=Horizontal vy= Vertical
self.vx = random.uniform(-3, 3)
self.vy = random.uniform(-15, -10)  # Lancé vers le haut (négatif)

self.is_sliced = False


def move(self):
    self.vy += GRAVITY  # ralenti l'ascension
    self.x += self.vx
    self.y += self.vy


def slice(self):
    self.is_sliced = True
    print(f"{self.name} est coupé !")


# CLASS FILLES


class Fructs(GameObject):
    def __init__(self, points, name, x, y, key):
        self.name = name
        self.x = x
        self.y = y
        self.key = key
        self.is_sliced = False
        super().__init__(name, points=2)


class Bomb(GameObject):
    def __init__(points):
        super().__init__("BOMBE", points=0)


class Ice(GameObject):
    def __init__(points):
        super().__init__("ICE_CUBE", points=0)
