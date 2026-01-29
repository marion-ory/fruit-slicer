import random
from entities import random_fruit, bomb, ice_cube, goldenfruit


class BeatSpawner:
    def __init__(self, beat_times_ms, difficulty="EASY"):
        self.beat_times_ms = beat_times_ms
        self.beat_index = 0
        self.difficulty = difficulty
        
        if difficulty == "EASY":
            self.bomb_chance = 0.08
            self.ice_chance = 0.05
            self.golden_chance = 0.08
            self.fruit_per_beat = 1
            self.spawn_skip_chance = 0.30
        else:
            self.bomb_chance = 0.18
            self.ice_chance = 0.06
            self.golden_chance = 0.09
            self.fruit_per_beat = 2
            self.spawn_skip_chance = 0.20
    
    def update(self, elapsed_ms, objects):
        while self.beat_index < len(self.beat_times_ms):
            beat_time = self.beat_times_ms[self.beat_index]
            if elapsed_ms >= beat_time:
                self.beat_index += 1
                
                if random.random() < self.spawn_skip_chance:
                    continue
                
                for _ in range(self.fruit_per_beat):
                    rand = random.random()
                    
                    if rand < self.bomb_chance:
                        objects.append(bomb())
                    elif rand < self.bomb_chance + self.ice_chance:
                        objects.append(ice_cube())
                    elif rand < self.bomb_chance + self.ice_chance + self.golden_chance:
                        objects.append(goldenfruit())
                    else:
                        objects.append(random_fruit())
            else:
                break
