from game_functions import *
from colorama import init

def main():
    init(autoreset=True)
    intro()
    while True:
        action = get_player_choice()
        if action.lower() == 'quit':
            break
        process_action(action)
    outro()

if __name__ == "__main__":
    main()
