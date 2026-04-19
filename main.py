"""
This is the main file for the Steam card simulator.
It contains the main function to run the simulator and the functions to view the user's card collection, save and load the collection.

Pawel & Veikka
"""

import state #contains the list of games and their respective card drops and drop rates
import simulation #contains the function to simulate card drops
import storage #contains functions to save and load the state of the simulator, such as the user's card collection and the games they have played
import utils #contains utility functions for the simulator, such as checking for card drops and calculating progress towards completing a card collection


def main():
    saved_state = storage.load_state()
    collection = saved_state.get("collection", [])  # In-memory collection for this run
    balance = saved_state.get("balance", 0)  # gems earned from selling cards
    print("Steam card simulator")
    
    while True:
        print('\033c', end='') # Clear the console for better readability
        print("Available games:")
        
        for idx, games in enumerate(state.games):  # print the list of games with their respective indices
            print(f"{idx + 1}. {games['name']}")
        
        raw_choice = input("Select a game to play by entering its number: ").strip()
        if not raw_choice.isdigit():
            print("Invalid entry. Please enter a game number.")
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
                
                progress = utils.calculate_progress(collection, sum(game["total_cards"] for game in state.games))
                print(f"Progress towards completing a card collection: {progress:.2f}%")
                
                game_progress = utils.calculate_game_progress(collection, selected_game)
                print(f"Progress for {selected_game['name']}: {game_progress:.2f}%")

            else:
                print("You didn't receive any cards. Play more to increase your chances!")
            
            while True:
                continue_choice = input("Play another game (y), view inventory (n), exit (e): ").strip().lower()

                if continue_choice == 'e':
                    print("Exiting the simulator. Goodbye!")
                    return
                
                if continue_choice == 'y':
                    break
                
                elif continue_choice == 'n':
                    print('\033c', end='')
                    
                    if collection:
                        print("Your card collection:")
                        total_collection_value = 0
                        
                        for card in collection:
                            total_collection_value += card.get("value", 0)
                            rarity_label = card.get("rarity", "common").capitalize()
                            
                            if rarity_label == "Rare":
                                print(f"- {card['name']} [{rarity_label}] ({card.get('value', 0)} gems)")
                            
                            else:
                                print(f"- {card['name']} ({card.get('value', 0)} gems)")
                        print(f"Total collection value: {total_collection_value} gems")
                    else:
                        print("Your card collection is empty.")
                        print("Total collection value: 0 gems")

                    print("Progress per game:")
                    for game in state.games:
                        progress = utils.calculate_game_progress(collection, game)
                        print(f"- {game['name']}: {progress:.2f}%")
                    print("sell cards: press 's' to sell cards for gems")
                    print(f"current gem balance: {balance} gems")
                    print("save collection: press 'v' to save your collection")
                    print("load collection: press 'l' to load your collection")
                    print("delete saved collection: press 'd' to delete saved cards and balance")
                    print("play again: press 'p' to play another game")
                    print("exit: press 'e' to exit the simulator")
                    
                    while True:
                        action = input("Enter your choice: ").strip().lower()
                        if action == 's':
                            if collection:
                                sale_amount = sum(card.get("value", 0) for card in collection)
                                balance += sale_amount
                                collection = []
                                storage.save_state(collection, balance)
                                print(f"Sold all cards for {sale_amount} gems.")
                                print(f"Current balance: {balance} gems.")
                            else:
                                print("No cards to sell.")
                        
                        elif action == 'v':
                            storage.save_state(collection, balance)
                            print("Collection saved.")                            
                        elif action == 'l':
                            loaded_state = storage.load_state()
                            collection = loaded_state.get("collection", [])
                            balance = loaded_state.get("balance", 0)
                            print("Collection and balance loaded.")
                        elif action == 'd':
                            storage.delete_state()
                            collection = []
                            balance = 0
                            print("Saved collection and balance deleted.")
                        elif action == 'p':
                            continue_choice = 'y'  # Set to 'y' to continue playing after viewing collection
                            break
                        
                        elif action == 'e':
                            print("Exiting the simulator. Goodbye!")
                            return
                        
                        else:
                            print("Invalid choice. Please enter 's', 'v', 'l', 'd', 'p' or 'e'.")
                continue

        else:
            print("No game found. Please select a valid game.")



#inventory management and saving/loading state and viewing collection can be implemented here using the storage module


#inventory management and saving/loading state and viewing collection can be implemented here using the storage module
#choose to implement additional features such as viewing the user's card collection, saving/loading the state of the simulator, and managing the user's inventory of cards.


if __name__ == "__main__":
    main()
