"""
This is the main file for the Steam card simulator.
It contains the main function to run the simulator and the functions to view the user's card collection, save and load the collection.

Pawel
"""

import state #contains the list of games and their respective card drops and drop rates
import simulation #contains the function to simulate card drops
import storage #contains functions to save and load the state of the simulator, such as the user's card collection and the games they have played

def main():
    collection = []  # In-memory collection for this run
    print("Steam card simulator")
    print("Available games:")
    
    for idx, games in enumerate(state.games):  # print the list of games with their respective indices
        print(f"{idx + 1}. {games['name']}")
    
    while True:
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
            else:
                print("You didn't receive any cards. Play more to increase your chances!")
            
            while True:
                continue_choice = input("Do you want to play another game? (y for yes, n for no): ").strip().lower()
                if continue_choice == 'y':
                    break
                elif continue_choice == 'n':
                    break
                else:
                    print("Invalid choice. Please enter 'y' or 'n'.")

            if continue_choice == 'y':
                continue
            else:
                break

        else:
            print("No game found. Please select a valid game.")
    
    for _ in range(10):  # Simulate 10 ticks of card drops for all games
        simulation.simulate_tick()
    
    while True:
        choice_view = input("Do you want to view your card collection? (y for yes, n for no): ").strip().lower()
        if choice_view == 'y':
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
        elif choice_view == 'n':
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")



#inventory management and saving/loading state and viewing collection can be implemented here using the storage module


#inventory management and saving/loading state and viewing collection can be implemented here using the storage module
#choose to implement additional features such as viewing the user's card collection, saving/loading the state of the simulator, and managing the user's inventory of cards.


if __name__ == "__main__":
    main()
