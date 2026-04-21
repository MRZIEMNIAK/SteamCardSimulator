"""
This is the main file for the Steam card simulator.
It contains the main function to run the simulator and the functions to view the user's card collection, save and load the collection.

Pawel & Veikka
"""

import state #contains the list of games and their respective card drops and drop rates
import simulation #contains the function to simulate card drops
import storage #contains functions to save and load the state of the simulator, such as the user's card collection and the games they have played
import utils #contains utility functions for the simulator, such as checking for card drops and calculating progress towards completing a card collection


# The main function to run the simulator, allowing the user to select games, view possible card drops, manage their inventory, and save/load their collection and balance.
def main():
    
    print("")
    saved_state = storage.load_state()
    collection = saved_state.get("collection", [])  # In-memory collection for this run
    balance = saved_state.get("balance", 0)  # gems earned from selling cards
    state.games = saved_state.get("games", state.games)
    print("Steam card simulator")
    
    while True: #main loop of the simulator.
        print("\033c", end="") # Clear the console for better readability
        print("====WELCOME TO CARD SIMULATOR====")
        print("Enter 'o' to view all possible card drops")
        print("Enter 'i' to view inventory")
        print("Enter 'e' to exit")
        print(" ")
        print("===GAMES===")
        for idx, games in enumerate(state.games):  # print the list of games with their respective indices
            print(f"{idx + 1}. {games['name']}")
        
        print(" ")
        raw_choice = input("Select a game to play or make changes: ").strip() 
        if raw_choice.lower() == 'o':
            view_possible_card_drops()
            continue


        if raw_choice.lower() == 'q':
            collection, balance, outcome = open_edit_inventory_menu(collection, balance)
            continue
        
        if raw_choice.lower() == 'i':
            collection, balance, outcome = open_inventory_menu(collection, balance)

            if outcome == "edit":
                collection, balance, _ = open_edit_inventory_menu(collection, balance)
                continue

            if outcome == "exit":
                print("Exiting the simulator. Goodbye!")
                return
            continue


        if raw_choice.lower() == 'e':
            utils.save_all_state(collection, balance)
            print("Exiting the simulator. Goodbye!")
            return

        if not raw_choice.isdigit():
            print("Invalid entry. Try again: ") #preventing invalid input when selecting a game. 
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
                utils.save_all_state(collection, balance)
                
                progress = utils.calculate_progress(collection, sum(game["total_cards"] for game in state.games))
                print(f"Progress towards completing a card collection: {progress:.2f}%")
                
                game_progress = utils.calculate_game_progress(collection, selected_game)
                print(f"Progress for {selected_game['name']}: {game_progress:.2f}%")

            else:
                print("You didn't receive any cards. Play more to increase your chances!")
            
            while True:
                continue_choice = input("Play another game (y), view inventory (n), exit (e): ").strip().lower()

                if continue_choice == 'e':
                    utils.save_all_state(collection, balance)
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


def open_edit_inventory_menu(collection, balance):
    print("\033c", end="")
    print("====EDIT CARDS====")
    print(" ")
    print("Press 'a' to add a new game")
    print("Press 'c' to add a card to game")
    print("Press 'g' to remove game from pool")
    print("Press 'x' to remove card from pool")
    print("Press 'r' to remove card from inventory")
    print("Press 'i' to return to inventory")
    print(" ")

    while True:
        action = utils.get_valid_choice({'a','c','g','x','r','i','q'})

        if action == 'a':
            storage.add_game(collection, balance)
        elif action == 'c':
            storage.add_card_to_game(collection, balance)
        elif action == 'g':
            storage.remove_game_from_pool(collection, balance)
        elif action == 'x':
            storage.remove_card_from_game_pool(collection, balance)
        elif action == 'r':
            remove_card_from_inventory(collection, balance)
        elif action == 'i':
            return collection, balance, "inventory"
        elif action == 'q':
            return collection, balance, "main"
        else:
            print("Invalid choice.")

# Additional functions to manage the inventory, view possible card drops
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
    utils.save_all_state(collection, balance) #saving the state after removing the card from inventory.
    print(f"Removed '{removed_card['name']}' from inventory.")


def view_possible_card_drops(): #function to view the possible card drops for each game in the simulator, including their drop rates and values.
    print("\033c", end="")
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

#functions to manage the inventory and the games and cards in the drop pool.
def print_inventory(collection, balance): #function to print the user's card collection, progress towards completing collections, and available actions in the inventory menu.
    print("\033c", end="")
    print("====INVENTORY====")

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
        
    print(f"current gem balance: {balance} gems")
    print(" ")
    print("Progress per game:") #calculating and printing the progress towards completing the card collection for each game in the simulator.
    for game in state.games:
        progress = utils.calculate_game_progress(collection, game) #pull data for each game and calculate the progress.
        print(f"- {game['name']}: {progress:.2f}%")
        
#printing the available actions in the inventory menu and the user's current gem balance.
    print(" ")
    print("Press 's' to sell cards")
    print("Press 'v' to save your inventory")
    print("Press 'l' to load your inventory")
    print("Press 'd' to delete saved collection")
    print("Press 'p' to play another game")
    print("Press 'q' to edit the inventory")
    print("Press 'e' to exit the simulator")


#functions to manage the inventory and the games and cards in the drop pool.
def open_inventory_menu(collection, balance): #func to open inventory menu.
    while True:
        print_inventory(collection, balance)
        print(" ")
        action = utils.get_valid_choice({'s','v','l','d','p','q','e'})


        if action == 's': #command to sell all cards in inventory for gems.
            if collection:
                sale_amount = sum(card.get("value", 0) for card in collection)
                balance += sale_amount
                collection = []
                utils.save_all_state(collection, balance)
                print(f"Sold all cards for {sale_amount} gems.")
                print(f"Current balance: {balance} gems.")
            else:
                print("\nNo cards to sell.")
                input("\nContinue")

        elif action == 'v': #command to save the inventory and balance to storage.
            utils.save_all_state(collection, balance)
            print("\nInventory saved.")
            input("\nContinue")
        elif action == 'l': #command to load the inventory and balance from storage, replacing the current in-memory collection and balance with the loaded data.
            loaded_state = storage.load_state()
            collection = loaded_state.get("collection", [])
            balance = loaded_state.get("balance", 0)
            state.games = loaded_state.get("games", state.games)
            print("\nInventory and balance loaded.")
            input("\nContinue")
        elif action == 'd': #command to delete the saved collection and balance. Works as reset for the simulator, since it deletes the saved state and resets the in-memory collectiona and balance to 0.
            storage.delete_state()
            collection = []
            balance = 0
            print("Saved collection and balance deleted.")
            input("\nContinue")
        
        elif action == 'p':
            return collection, balance, "play"

        elif action == 'q':
            return collection, balance, "edit"

        elif action == 'e':
            utils.save_all_state(collection, balance)
            return collection, balance, "exit"


        
            
        




#inventory management and saving/loading state and viewing collection can be implemented here using the storage module
#choose to implement additional features such as viewing the user's card collection, saving/loading the state of the simulator, and managing the user's inventory of cards.


if __name__ == "__main__":
    main()



####IDEAS#####
#Merge all game to one line for example Mirage x2 (10)
#Play games without asking to play again 'y'? Loop unlimited gambling
#Inspect the code and delete useless stuff, example useless and complicated code from storage
#
#####ISSUE#####
#Farming cards from one game constantly increases the completition, even over 100%
#Sometimes play another game straight from inventory feels wonky
#Not all error codes appear
#Untested error
