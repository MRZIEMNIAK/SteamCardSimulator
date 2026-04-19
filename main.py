"""
This is the main file for the Steam card simulator.
It contains the main function to run the simulator and the functions to view the user's card collection, save and load the collection.

Pawel & Veikka
"""

import state #contains the list of games and their respective card drops and drop rates
import simulation #contains the function to simulate card drops
import storage #contains functions to save and load the state of the simulator, such as the user's card collection and the games they have played
import utils #contains utility functions for the simulator, such as checking for card drops and calculating progress towards completing a card collection


def save_all_state(collection, balance):
    storage.save_state(collection, balance, state.games)


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
    save_all_state(collection, balance) #saving the new game to storage after adding it to state.
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
    save_all_state(collection, balance)
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

    save_all_state(collection, balance) #saving the state after removing the game and the cards from inventory.
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

    save_all_state(collection, balance) #saving the state after removing the card from the game pool and inventory.
    print(f"Removed card '{removed_card['name']}' from {selected_game['name']}.")
    print(f"Removed {removed_from_inventory} matching card(s) from inventory.")


def remove_card_from_inventory(collection, balance): #removing card from inventory
    if not collection:
        print("Inventory is empty.")
        return

    print("Select an inventory card to remove:") #listing the cards in inventory to choose from for removal.
    for idx, card in enumerate(collection):
        rarity_label = card.get("rarity", "common").capitalize()
        print(f"{idx + 1}. {card['name']} [{rarity_label}] ({card.get('value', 0)} gems)")

    raw_choice = input("Enter the card number: ").strip()
    if not raw_choice.isdigit():
        print("Invalid card number.") #preventing invalid card numbers.
        return

    card_choice = int(raw_choice)
    if not 1 <= card_choice <= len(collection):
        print("Invalid card number.")
        return

    removed_card = collection.pop(card_choice - 1)
    save_all_state(collection, balance) #saving the state after removing the card from inventory.
    print(f"Removed '{removed_card['name']}' from inventory.")


def view_possible_card_drops(): #function to view the possible card drops for each game in the simulator, including their drop rates and values.
    print('\033c', end='')
    print("Possible card drops by game:")

    for game in state.games:
        print(f"\n{game['name']}:")

        regular_cards = game.get("cards", [])
        rare_cards = game.get("rare_cards", [])

        if regular_cards:
            print("  Common cards:")
            for card in regular_cards:
                print(f"  - {card['name']} ({card.get('drop_rate', 0)} drop rate, {card.get('value', 0)} gems)")
        else:
            print("  Common cards: none")

        if rare_cards:
            print("  Rare cards:")
            for card in rare_cards:
                print(f"  - {card['name']} ({card.get('drop_rate', 0)} drop rate, {card.get('value', 0)} gems)")
        else:
            print("  Rare cards: none")

    input("\nPress Enter to return to the main menu...") 


def print_inventory(collection, balance): #function to print the user's card collection, progress towards completing collections, and available actions in the inventory menu.
    print('\033c', end='')

    if collection: 
        print("Your card collection:")
        total_collection_value = 0

        for card in collection: #calculating the total value of the user's cards.
            total_collection_value += card.get("value", 0)
            rarity_label = card.get("rarity", "common").capitalize()

            if rarity_label == "Rare": #sorting the cards in inventory by rarity and printing them with their values.
                print(f"- {card['name']} [{rarity_label}] ({card.get('value', 0)} gems)")

            else:
                print(f"- {card['name']} ({card.get('value', 0)} gems)")
        print(f"Total collection value: {total_collection_value} gems")
    else:
        print("Your card collection is empty.") #if the collection is empty, print that instead of trying to calculate the total value and progress, which would be 0 anyway.
        print("Total collection value: 0 gems") #printing the total collection value as 0 when the collection is empty.

    print("Progress per game:") #calculating and printing the progress towards completing the card collection for each game in the simulator.
    for game in state.games:
        progress = utils.calculate_game_progress(collection, game) #pull data for each game and calculate the progress.
        print(f"- {game['name']}: {progress:.2f}%")
#printing the available actions in the inventory menu and the user's current gem balance.
    print("sell cards: press 's' to sell cards for gems")
    print(f"current gem balance: {balance} gems")
    print("save inventory: press 'v' to save your inventory")
    print("load inventory: press 'l' to load your inventory")
    print("delete saved collection: press 'd' to delete saved cards and balance")
    print("add game: press 'a' to add a new game")
    print("add card: press 'c' to add a card to a game")
    print("remove game from pool: press 'g'")
    print("remove card from pool: press 'x'")
    print("remove card from inventory: press 'r'")
    print("play again: press 'p' to play another game")
    print("exit: press 'e' to exit the simulator")

#functions to manage the inventory and the games and cards in the drop pool.
def open_inventory_menu(collection, balance): #func to open inventory menu.
    while True:
        print_inventory(collection, balance)
        action = input("Enter your choice: ").strip().lower()

        if action == 's': #command to sell all cards in inventory for gems.
            if collection:
                sale_amount = sum(card.get("value", 0) for card in collection)
                balance += sale_amount
                collection = []
                save_all_state(collection, balance)
                print(f"Sold all cards for {sale_amount} gems.")
                print(f"Current balance: {balance} gems.")
            else:
                print("No cards to sell.")

        elif action == 'v': #command to save the inventory and balance to storage.
            save_all_state(collection, balance)
            print("Inventory saved.")
        elif action == 'l': #command to load the inventory and balance from storage, replacing the current in-memory collection and balance with the loaded data.
            loaded_state = storage.load_state()
            collection = loaded_state.get("collection", [])
            balance = loaded_state.get("balance", 0)
            state.games = loaded_state.get("games", state.games)
            print("Inventory and balance loaded.")
        elif action == 'd': #command to delete the saved collection and balance. Works as reset for the simulator, since it deletes the saved state and resets the in-memory collectiona and balance to 0.
            storage.delete_state()
            collection = []
            balance = 0
            print("Saved collection and balance deleted.")
        elif action == 'a':
            add_game(collection, balance)
        elif action == 'c':
            add_card_to_game(collection, balance)
        elif action == 'g':
            remove_game_from_pool(collection, balance)
        elif action == 'x':
            remove_card_from_game_pool(collection, balance)
        elif action == 'r':
            remove_card_from_inventory(collection, balance)
        elif action == 'p':
            return collection, balance, "play"

        elif action == 'e':
            save_all_state(collection, balance)
            return collection, balance, "exit"

        else:
            print("Invalid choice. Please enter 's', 'v', 'l', 'd', 'a', 'c', 'g', 'x', 'r', 'p' or 'e'.") #preventing invalid input in the inventory menu. Only accepting the specified commands.

# The main function to run the simulator, allowing the user to select games, view possible card drops, manage their inventory, and save/load their collection and balance.
def main():
    saved_state = storage.load_state()
    collection = saved_state.get("collection", [])  # In-memory collection for this run
    balance = saved_state.get("balance", 0)  # gems earned from selling cards
    state.games = saved_state.get("games", state.games)
    print("Steam card simulator")
    
    while True: #main loop of the simulator.
        print('\033c', end='') # Clear the console for better readability
        print("Available games:")
        print("Enter 'o' to view all possible card drops")
        print("Enter 'i' to view inventory")
        print("Enter 'e' to exit")
        
        for idx, games in enumerate(state.games):  # print the list of games with their respective indices
            print(f"{idx + 1}. {games['name']}")
        
        raw_choice = input("Select a game to play by entering its number: ").strip() 
        if raw_choice.lower() == 'o':
            view_possible_card_drops()
            continue

        if raw_choice.lower() == 'i':
            collection, balance, outcome = open_inventory_menu(collection, balance)
            if outcome == "exit":
                print("Exiting the simulator. Goodbye!")
                return
            continue

        if raw_choice.lower() == 'e':
            save_all_state(collection, balance)
            print("Exiting the simulator. Goodbye!")
            return

        if not raw_choice.isdigit():
            print("Invalid entry. Please enter a game number.") #preventing invalid input when selecting a game. 
            continue

        choice = int(raw_choice)
        if 1 <= choice <= len(state.games):  # check if the user's choice is valid
            selected_game = state.games[choice - 1]  # get the selected game based on the user's choice
            drops = simulation.simulate_card_drops(selected_game)  # simulate the card drops for the selected game
            
            if drops:
                print("You received the following cards:")
                round_total_value = 0
                
                for cards in drops:
                    round_total_value += cards.get("value", 0)
                    rarity_label = cards.get("rarity", "common").capitalize()
                    
                    if rarity_label == "Rare":
                        print(f"- {cards['name']} [{rarity_label}] ({cards.get('value', 0)} gems)")
                    
                    else:
                        print(f"- {cards['name']} ({cards.get('value', 0)} gems)")
                print(f"Total value this round: {round_total_value} gems")
                collection.extend(drops)  # Add drops to in-memory collection
                save_all_state(collection, balance)
                
                progress = utils.calculate_progress(collection, sum(game["total_cards"] for game in state.games))
                print(f"Progress towards completing a card collection: {progress:.2f}%")
                
                game_progress = utils.calculate_game_progress(collection, selected_game)
                print(f"Progress for {selected_game['name']}: {game_progress:.2f}%")

            else:
                print("You didn't receive any cards. Play more to increase your chances!")
            
            while True:
                continue_choice = input("Play another game (y), view inventory (n), exit (e): ").strip().lower()

                if continue_choice == 'e':
                    save_all_state(collection, balance)
                    print("Exiting the simulator. Goodbye!")
                    return
                
                if continue_choice == 'y':
                    break
                
                elif continue_choice == 'n':
                    collection, balance, outcome = open_inventory_menu(collection, balance)
                    if outcome == "exit":
                        print("Exiting the simulator. Goodbye!")
                        return
                    continue_choice = 'y'
                continue

        else:
            print("No game found. Please select a valid game.")



#inventory management and saving/loading state and viewing collection can be implemented here using the storage module


#inventory management and saving/loading state and viewing collection can be implemented here using the storage module
#choose to implement additional features such as viewing the user's card collection, saving/loading the state of the simulator, and managing the user's inventory of cards.


if __name__ == "__main__":
    main()
