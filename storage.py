import json
import os

SAVE_FILE = "collection.json"  # File to save/load the collection

def save_collection(collection):
    """Save the user's card collection to a JSON file without overwriting existing cards."""
    try:
        existing = []
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                existing = json.load(f)
            if not isinstance(existing, list):
                existing = []

        existing_keys = {(card.get("name"), card.get("rarity")) for card in existing}
        new_cards = [card for card in collection if (card.get("name"), card.get("rarity")) not in existing_keys]
        combined_collection = existing + new_cards

        with open(SAVE_FILE, 'w') as f:
            json.dump(combined_collection, f, indent=4)

        if new_cards:
            print(f"Collection saved successfully. Added {len(new_cards)} new card(s).")
        else:
            print("Collection saved successfully. No new cards were added.")
    except Exception as e:
        print(f"Error saving collection: {e}")


def load_collection():
    """Load the user's card collection from a JSON file."""
    if not os.path.exists(SAVE_FILE):
        print("No saved collection found. Starting with an empty collection.")
        return []
    try:
        with open(SAVE_FILE, 'r') as f:
            collection = json.load(f)
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
        return collection
    except Exception as e:
        print(f"Error loading collection: {e}")
        return []
