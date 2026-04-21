"""
The storage code saves and loads the game's state (cards, balance, and games) to a JSON file so progress persists between runs.

Daniel
"""
import json
import os
import copy
import state
import utils

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

        #print("Collection saved successfully.")
        #print(f"Saved gem balance: {balance} gems.")
    except Exception as e:
        print(f"Error saving collection: {e}")


def load_state():
    """Load the user's card collection, gem balance, and game catalog from a JSON file."""
    if not os.path.exists(SAVE_FILE):
        print("No saved collection found. Starting with an empty collection.")
        input("\nContinue")
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


def add_game(collection, balance): #Add new game to the simulator.
    game_name = input("Enter new game name: ").strip()
    if not game_name:
        print("Game name cannot be empty.")
        return

    if any(game["name"].lower() == game_name.lower() for game in state.games): #preventing duplicates.
        print("That game already exists.")
        return

    next_game_id = max((game.get("id", 0) for game in state.games), default=0) + 1 #saving the game to state and then to storage.
    state.games.append(
        {
            "id": next_game_id,
            "name": game_name,
            "cards": [],
            "rare_cards": [],
            "total_cards": 0,
        }
    )
    utils.save_all_state(collection, balance) #saving the new game to storage after adding it to state.
    print(f"Added game: {game_name}")

def add_card_to_game(collection, balance): #Add new card to a game in the simulator.
    if not state.games:
        print("No games exist yet. Add a game first.") #preventing adding cards to non-existent games.
        return

    print("Select a game to add a card to:") #input to select a game you want to add the card to.
    for idx, game in enumerate(state.games):
        print(f"{idx + 1}. {game['name']}")

    raw_choice = input("Enter the game number: ").strip() #selecting the game by its number.
    if not raw_choice.isdigit():
        print("Invalid game number.")
        return

    game_choice = int(raw_choice) #checking if the selected game number is valid.
    if not 1 <= game_choice <= len(state.games):
        print("Invalid game number.")
        return
    
#setting the card name, rarity, drop rate and value for the new card. Then saving it to state and storage.
    selected_game = state.games[game_choice - 1] 
    card_name = input("Enter card name: ").strip() 
    if not card_name:
        print("Card name cannot be empty.")
        return

    rarity = input("Enter rarity (common/rare): ").strip().lower()
    if rarity not in {"common", "rare"}:
        print("Invalid rarity. Use common or rare.")
        return

    raw_drop_rate = input("Enter drop rate between 0 and 1: ").strip() #preventing too high droprates and invalid input.
    try:
        drop_rate = float(raw_drop_rate)
    except ValueError:
        print("Invalid drop rate.")
        return

    if not 0 < drop_rate <= 1:
        print("Drop rate must be greater than 0 and at most 1.")
        return

    default_value = 10 if rarity == "rare" else 5
    raw_value = input(f"Enter card value (press enter for {default_value}): ").strip()
    if raw_value:
        try:
            card_value = int(raw_value)
        except ValueError:
            print("Invalid card value.")
            return
    else:
        card_value = default_value

    target_cards = selected_game["rare_cards"] if rarity == "rare" else selected_game["cards"]
    next_card_id = max((card.get("id", 0) for card in target_cards), default=0) + 1
    target_cards.append(
        {
            "id": next_card_id,
            "name": card_name,
            "drop_rate": drop_rate,
            "rarity": rarity,
            "value": card_value,
        }
    )
    selected_game["total_cards"] = len(selected_game.get("cards", [])) + len(selected_game.get("rare_cards", []))
    utils.save_all_state(collection, balance)
    print(f"Added {rarity} card '{card_name}' to {selected_game['name']}.")


    #removing games and cards from the drop pool and inventory management functions below.
def remove_game_from_pool(collection, balance): #removing game
    if not state.games:
        print("No games available to remove.")
        return

    print("Select a game to remove from the drop pool:")
    for idx, game in enumerate(state.games):
        print(f"{idx + 1}. {game['name']}")

    raw_choice = input("Enter the game number: ").strip()
    if not raw_choice.isdigit():
        print("Invalid game number.")
        return

    game_choice = int(raw_choice) #preventing invalid game numbers.
    if not 1 <= game_choice <= len(state.games):
        print("Invalid game number.")
        return

    removed_game = state.games.pop(game_choice - 1)
    removed_card_names = {
        card["name"]
        for card in removed_game.get("cards", []) + removed_game.get("rare_cards", [])
    }
    removed_count = len(collection)
    collection[:] = [card for card in collection if card.get("name") not in removed_card_names]
    removed_from_inventory = removed_count - len(collection)

    utils.save_all_state(collection, balance) #saving the state after removing the game and the cards from inventory.
    print(f"Removed game '{removed_game['name']}' from the drop pool.")
    print(f"Removed {removed_from_inventory} matching card(s) from inventory.")


def remove_card_from_game_pool(collection, balance): #removing card from game pool
    if not state.games:
        print("No games available.")
        return

    print("Select a game:")    
    for idx, game in enumerate(state.games):
        print(f"{idx + 1}. {game['name']}")

    raw_choice = input("Enter the game number: ").strip()
    if not raw_choice.isdigit():
        print("Invalid game number.") #preventing invalid game numbers.
        return

    game_choice = int(raw_choice)
    if not 1 <= game_choice <= len(state.games):
        print("Invalid game number.")
        return

    selected_game = state.games[game_choice - 1]
    card_entries = []

    for idx, card in enumerate(selected_game.get("cards", [])): #creating a list of cards in the selected game to choose from for removal.
        card_entries.append(("cards", idx, card))
    for idx, card in enumerate(selected_game.get("rare_cards", [])):
        card_entries.append(("rare_cards", idx, card))

    if not card_entries:
        print("This game has no cards to remove.") #preventing trying to remove cards from a game that has no cards.
        return

    print(f"Cards in {selected_game['name']}:")
    for idx, (_, _, card) in enumerate(card_entries):
        rarity_label = card.get("rarity", "common").capitalize()
        print(f"{idx + 1}. {card['name']} [{rarity_label}] ({card.get('drop_rate', 0)} drop rate)")

    raw_card_choice = input("Enter the card number to remove: ").strip()
    if not raw_card_choice.isdigit():
        print("Invalid card number.")
        return

    card_choice = int(raw_card_choice)
    if not 1 <= card_choice <= len(card_entries):
        print("Invalid card number.")
        return

    list_name, index_in_list, removed_card = card_entries[card_choice - 1]
    selected_game[list_name].pop(index_in_list)
    selected_game["total_cards"] = len(selected_game.get("cards", [])) + len(selected_game.get("rare_cards", []))

    removed_count = len(collection) #removing the card from inventory if it exists there. This will remove all copies of the card from inventory, if there are multiple.
    collection[:] = [card for card in collection if card.get("name") != removed_card["name"]]
    removed_from_inventory = removed_count - len(collection)

    utils.save_all_state(collection, balance) #saving the state after removing the card from the game pool and inventory.
    print(f"Removed card '{removed_card['name']}' from {selected_game['name']}.")
    print(f"Removed {removed_from_inventory} matching card(s) from inventory.")