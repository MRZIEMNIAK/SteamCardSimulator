import json
import os

SAVE_FILE = "collection.json"  # File to save/load the collection

def save_collection(collection):
    """Save the user's card collection to a JSON file."""
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(collection, f, indent=4)
        print("Collection saved successfully.")
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
        return collection
    except Exception as e:
        print(f"Error loading collection: {e}")
        return []
