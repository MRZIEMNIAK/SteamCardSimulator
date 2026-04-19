import json
import os

SAVE_FILE = "collection.json"  # File to save/load the collection

def save_state(collection, balance):
    """Save the user's card collection and gem balance to a JSON file."""
    try:
        state_data = {
            "collection": collection,
            "balance": balance,
        }

        with open(SAVE_FILE, 'w') as f:
            json.dump(state_data, f, indent=4)

        print("Collection saved successfully.")
        print(f"Saved gem balance: {balance} gems.")
    except Exception as e:
        print(f"Error saving collection: {e}")


def load_state():
    """Load the user's card collection and gem balance from a JSON file."""
    if not os.path.exists(SAVE_FILE):
        print("No saved collection found. Starting with an empty collection.")
        return {"collection": [], "balance": 0}

    try:
        with open(SAVE_FILE, 'r') as f:
            state_data = json.load(f)

        if isinstance(state_data, list):
            collection = state_data
            balance = 0
        elif isinstance(state_data, dict):
            collection = state_data.get("collection", []) if isinstance(state_data.get("collection", []), list) else []
            balance = state_data.get("balance", 0)
        else:
            collection = []
            balance = 0

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
        return {"collection": collection, "balance": balance}
    except Exception as e:
        print(f"Error loading collection: {e}")
        return {"collection": [], "balance": 0}
