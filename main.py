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
        choice = int(input("Select a game by entering its number: "))  # get the user's choice of game
        if 1 <= choice <= len(state.games):  # check if the user's choice is valid
            selected_game = state.games[choice - 1]  # get the selected game based on the user's choice
            drops = simulation.simulate_card_drops(selected_game)  # simulate the card drops for the selected game
            if drops:
                print("You received the following cards:")
                for cards in drops:
                    print(f"- {cards}")
                collection.extend(drops)  # Add drops to in-memory collection
            else:
                print("No cards remaining.")
            
            continue_choice = input("Do you want to select another game? (y for yes, n for no): ").lower()
            if continue_choice == 'y':
                continue
            elif continue_choice == 'n':
                break
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")
        else:
            print("Invalid choice. Please select a valid game number.")
    
    for _ in range(10):  # Simulate 10 ticks of card drops for all games
        simulation.simulate_tick()
    
    while True:
        choice_view = input("Do you want to view your card collection? (y for yes, n for no): ").lower()
        if choice_view == 'y':
            if collection:
                print("Your card collection:")
                for card in collection:
                    print(f"- {card}")
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
