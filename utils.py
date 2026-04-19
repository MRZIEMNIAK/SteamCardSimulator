"""
Utility functions for the Steam Card Simulator.


Otso
"""

# max tick, save file, load file, 
# Muuttujat ja muuttumattomat arvot simulaatioon.

import storage
import state



MAX_TICK = 10 # suurin tick speedi. (Saa muuttaa tarpeiden mukaan)
DEFAULT_DROP_RATE = 0.005 # droprate, joka on 0.5% (Muuta jos tarvii)
PROBABLITY_PRECISION = 4 # kuinka monta desimaalia käytetään dropraten laskussa (Muuta jos tarvii) niiku esim 0.0050 tai 0.00500 jne
MIN_CARDS_PER_GAME = 0 # minimimäärä kortteja per peli (Muuta jos tarvii)
MAX_CARDS_PER_GAME = 6 # maksimimäärä kortteja per peli (Muuta jos tarvii)


def check_success(drop_rate):
    # Simuloi korttipudotusta vertaamalla satunnaislukua droprateen, toivottavasti XD
    import random
    return random.random() < drop_rate


def generate_card_collection(game_name, num_cards):
    # Luo korttikokoelman pelille, jossa on num_cards kortteja.
    return [f"{game_name} Card {i+1}" for i in range(num_cards)]

def calculate_progress(dropped_cards, total_cards):
    # Laskee korttikokoelman edistymisen prosentteina.
    if total_cards == 0:
        return 0
    return (len(dropped_cards) / total_cards) * 100


def calculate_game_progress(collection, game):
    # Calculate progress for a specific game
    game_card_names = {card['name'] for card in game['cards'] + game['rare_cards']}
    collected_unique = {card['name'] for card in collection if card['name'] in game_card_names}
    return calculate_progress(list(collected_unique), game['total_cards'])


def load_collection():
    state_data = storage.load_state()  # load the user's card collection and balance from storage
    return state_data.get("collection", [])

def save_collection(collection, balance=0):
    return storage.save_state(collection, balance)  # save the user's card collection and balance to storage