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
            drops.append(cards["name"])
    return drops

def simulate_tick():
    for game in state.games:
        dropped = simulate_card_drops(game)
        game["total_cards"] += len(dropped)
