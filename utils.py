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
MIN_CARDS_PER_GAME = 5 # minimimäärä kortteja per peli (Muuta jos tarvii)
MAX_CARDS_PER_GAME = 10 # maksimimäärä kortteja per peli (Muuta jos tarvii)


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


def save_collection(collection):
    storage.save_collection(collection) #save the user's card collection to storage

def load_collection():
    return storage.load_collection() #load the user's card collection from storage
