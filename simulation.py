"""
This is the simulation file for the Steam card simulator.
It contains the functions to simulate card drops and ticks for the games in the simulator.

Pawel
"""


#steam card simulator
import random
import state #games is a list of games with their respective card drops and drop rates


def simulate_card_drops(game): 
    drops = []

    for cards in game["cards"]:
        if random.random() < cards["drop_rate"]:
            drops.append({"name": cards["name"], "rarity": cards.get("rarity", "common"), "value": cards.get("value", 5)})

    for cards in game.get("rare_cards", []):
        if random.random() < cards["drop_rate"]:
            drops.append({"name": cards["name"], "rarity": cards.get("rarity", "rare"), "value": cards.get("value", 10)})

    return drops


#Ticks are not implemented yet
def simulate_tick():
    all_drops = []
    for games in state.games:
        dropped = simulate_card_drops(games)
        games["total_cards"] += len(dropped)
        all_drops.extend(dropped)
    return all_drops
