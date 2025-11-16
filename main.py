import json
from support_functions import *

if __name__ == '__main__':

    with open('kaiba_battle_city.json', 'r') as f:
        deck_info = json.load(f)

    LLM_game = LLMGameState('.decks/kaiba_battle_city.json')

    # Example game loop
    while True:
        command = input("\nYour action: ")

        if command == "draw":
            LLM_game.draw_from_deck()

        elif command == "summon":
            # e.g., "summon Blue-Eyes White Dragon M attack"
            parts = command.split()
            card_name = " ".join(parts[1:-2])  # Everything between summon and position
            zone = parts[-2]  # L, M, or R
            position = parts[-1]  # attack or defense
            # ... summon logic

        elif command == "end":
            break

        elif command == "state":
            # Show me the encoded state
            encoded = game.get_llm_state()
            print(encoded)

        else:
            print("Unknown command")








