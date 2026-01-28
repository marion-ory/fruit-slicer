# spawner.py

import random
from entities import random_fruit, bomb, ice_cube, goldenfruit
from config import DIFFICULTY_SETTINGS

class BeatSpawner:
    def __init__(self, beat_times_ms, difficulty="EASY"):
        self.beat_times_ms = beat_times_ms
        self.index = 0
        self.settings = DIFFICULTY_SETTINGS[difficulty]
        self.beat_counter = 0  # compteur pour espacer les spawns

    def update(self, elapsed_ms, object_list):
        while (
            self.index < len(self.beat_times_ms)
            and elapsed_ms >= self.beat_times_ms[self.index]
        ):
            self.beat_counter += 1
            # Spawn seulement tous les 2 beats pour réduire la fréquence
            if self.beat_counter % 2 == 0:
                self.spawn_on_beat(object_list)
            self.index += 1

    def spawn_on_beat(self, object_list):
        fruit_count = self.settings["fruit_per_beat"]
        for _ in range(fruit_count):
            object_list.append(random_fruit())

        if random.random() < self.settings["bomb_chance"]:
            object_list.append(bomb())

        if random.random() < 0.05:
            object_list.append(ice_cube())

        if random.random() < 0.03:
            object_list.append(goldenfruit())
