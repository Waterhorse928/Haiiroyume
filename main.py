import time
import math

class Character:
    def __init__(self, name, base_stats, growth_rates):
        self.name = name
        self.level = 1
        self.growth_rates = growth_rates
        self.base_stats = base_stats
        self.stats = self.calculate_stats()
        self.turn_bar = 0

    def calculate_stats(self):
        stats = {}
        for stat, growth_rate in self.growth_rates.items():
            stats[stat] = self.base_stats[stat] + self.level * growth_rate
        return stats
    
    def level_up(self):
        self.level += 1
        self.stats = self.calculate_stats()

    def update_turn_bar(self):
        self.turn_bar += self.stats['SPD'] / 10
        if self.turn_bar >= 100:
            self.turn_bar = 0
            # Trigger turn


def main_game_loop():
    character = Character("Player",base_stats,base_stats)

    while True:
        character.update_turn_bar()
        print("Turn bar:", math.floor(character.turn_bar))
        time.sleep(1)

base_stats = {
    "HP": 100,
    "SP": 50,
    "AP": 0,
    "STR": 5,
    "MAG": 5,
    "DEF": 5,
    "RES": 5,
    "SPD": 5,
    "SKL": 5,
    "EVA": 5,
    "LUK": 5
}

main_game_loop()