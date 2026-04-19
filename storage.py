import json
import os
import copy

import state

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "collection.json")  # File to save/load the collection

def save_state(collection, balance, games=None):
    """Save the user's card collection, gem balance, and game catalog to a JSON file."""
    try:
        state_data = {
            "collection": collection,
            "balance": balance,
            "games": games if games is not None else state.games,
        }

        with open(SAVE_FILE, 'w') as f:
            json.dump(state_data, f, indent=4)

        print("Collection saved successfully.")
        print(f"Saved gem balance: {balance} gems.")
    except Exception as e:
        print(f"Error saving collection: {e}")


def load_state():
    """Load the user's card collection, gem balance, and game catalog from a JSON file."""
    if not os.path.exists(SAVE_FILE):
        print("No saved collection found. Starting with an empty collection.")
        return {"collection": [], "balance": 0, "games": copy.deepcopy(state.games)}

    try:
        with open(SAVE_FILE, 'r') as f:
            state_data = json.load(f)

        if isinstance(state_data, list):
            collection = state_data
            balance = 0
            games = copy.deepcopy(state.games)
        elif isinstance(state_data, dict):
            collection = state_data.get("collection", []) if isinstance(state_data.get("collection", []), list) else []
            balance = state_data.get("balance", 0)
            games = state_data.get("games", copy.deepcopy(state.games))
            if not isinstance(games, list):
                games = copy.deepcopy(state.games)
        else:
            collection = []
            balance = 0
            games = copy.deepcopy(state.games)

        print("Collection loaded successfully.")
        if collection:
            print("Loaded collection:")
            total_value = 0
            for card in collection:
                total_value += card.get("value", 0)
                rarity_label = card.get("rarity", "common").capitalize()
                if rarity_label == "Rare":
                    print(f"- {card['name']} [{rarity_label}] ({card.get('value', 0)} gems)")
                else:
                    print(f"- {card['name']} ({card.get('value', 0)} gems)")
            print(f"Total collection value: {total_value} gems")
        else:
            print("Loaded collection is empty.")

        print(f"Loaded gem balance: {balance} gems")
        return {"collection": collection, "balance": balance, "games": games}
    except Exception as e:
        print(f"Error loading collection: {e}")
        return {"collection": [], "balance": 0, "games": copy.deepcopy(state.games)}


def delete_state():
    """Delete the saved state file so neither balance nor collection remain."""
    try:
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
            print("Saved collection deleted.")
        else:
            print("No saved collection file to delete.")
    except Exception as e:
        print(f"Error deleting saved collection: {e}")
